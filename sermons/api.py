from datetime import date
from datetime import timedelta
import hashlib
import json
import secrets

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.http import require_http_methods

from .models import (
    MAX_AUDIO_FILE_SIZE,
    Sermon,
    SermonCollection,
    SermonTag,
    SermonTranslation,
    TranslationJob,
)

MAX_REQUEST_BYTES = MAX_AUDIO_FILE_SIZE + (1024 * 1024)
TRANSLATION_JOB_TTL_SECONDS = 5 * 60
TRANSLATION_FIELDS = ("title", "summary", "thesis", "transcript")


def _unauthorized_response():
    return JsonResponse(
        {"error": "Invalid or missing API credentials."},
        status=401,
        headers={"WWW-Authenticate": "Bearer"},
    )


def _get_bearer_token(request):
    authorization = request.headers.get("Authorization", "")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return ""
    return token.strip()


def _parse_tags(request):
    values = request.POST.getlist("tags")
    if len(values) == 1:
        values = values[0].split(",")
    return [value.strip() for value in values if value.strip()]


def _authenticate(request):
    configured_key = getattr(settings, "SERMON_UPLOAD_API_KEY", "")
    token = _get_bearer_token(request)
    if not configured_key or not token:
        return _unauthorized_response()
    if not secrets.compare_digest(token, configured_key):
        return _unauthorized_response()
    return None


@csrf_exempt
@require_http_methods(["POST"])
def sermon_upload(request):
    """Create an authenticated, unpublished sermon draft from multipart form data."""
    content_length = request.META.get("CONTENT_LENGTH")
    if content_length:
        try:
            request_size = int(content_length)
        except ValueError:
            request_size = 0
        if request_size > MAX_REQUEST_BYTES:
            return JsonResponse(
                {"error": "Upload is too large. MP3 files must be 100 MB or smaller."},
                status=413,
            )

    authentication_error = _authenticate(request)
    if authentication_error:
        return authentication_error

    required_fields = (
        "title",
        "speaker",
        "sermon_date",
        "summary",
        "thesis",
        "main_scripture",
    )
    missing_fields = [
        field for field in required_fields if not request.POST.get(field, "").strip()
    ]
    if "media_file" not in request.FILES:
        missing_fields.append("media_file")
    if missing_fields:
        return JsonResponse(
            {"error": "Missing required fields.", "fields": missing_fields},
            status=400,
        )

    try:
        sermon_date = date.fromisoformat(request.POST["sermon_date"].strip())
    except ValueError:
        return JsonResponse(
            {"error": "sermon_date must use YYYY-MM-DD format."}, status=400
        )

    collection = None
    collection_slug = request.POST.get("collection", "").strip()
    if collection_slug:
        try:
            collection = SermonCollection.objects.get(slug=collection_slug)
        except SermonCollection.DoesNotExist:
            return JsonResponse(
                {"error": "Unknown collection.", "collection": collection_slug},
                status=400,
            )

    tags = []
    tag_slugs = _parse_tags(request)

    duration_seconds = None
    duration_value = request.POST.get("duration_seconds", "").strip()
    if duration_value:
        try:
            duration_seconds = int(duration_value)
        except ValueError:
            return JsonResponse(
                {"error": "duration_seconds must be an integer."}, status=400
            )
        if duration_seconds < 0:
            return JsonResponse(
                {"error": "duration_seconds cannot be negative."}, status=400
            )

    sermon = Sermon(
        title=request.POST["title"].strip(),
        speaker=request.POST["speaker"].strip(),
        sermon_date=sermon_date,
        summary=request.POST["summary"].strip(),
        thesis=request.POST["thesis"].strip(),
        main_scripture=request.POST["main_scripture"].strip(),
        transcript=request.POST.get("transcript", ""),
        collection=collection,
        duration_seconds=duration_seconds,
        media_file=request.FILES["media_file"],
        is_published=False,
    )

    try:
        sermon.full_clean()
    except ValidationError as error:
        return JsonResponse(
            {"error": "Sermon validation failed.", "fields": error.message_dict},
            status=400,
        )

    with transaction.atomic():
        if tag_slugs:
            tags_by_slug = {}
            for slug in tag_slugs:
                tag, _ = SermonTag.objects.get_or_create(
                    slug=slug,
                    defaults={"name": slug.replace("-", " ").title()},
                )
                tags_by_slug[slug] = tag
            tags = [tags_by_slug[slug] for slug in tag_slugs]
        sermon.save()
        if tags:
            sermon.tags.set(tags)

    return JsonResponse(
        {
            "id": sermon.pk,
            "slug": sermon.slug,
            "is_published": sermon.is_published,
            "message": "Sermon draft created.",
        },
        status=201,
    )


@csrf_exempt
@require_http_methods(["GET"])
def collection_list(request):
    """Return existing sermon collections for the trusted uploader."""
    authentication_error = _authenticate(request)
    if authentication_error:
        return authentication_error

    collections = SermonCollection.objects.order_by("name").values(
        "id", "name", "slug", "description", "is_published"
    )
    return JsonResponse({"collections": list(collections)})


def _translation_source(sermon, field):
    return getattr(sermon, field, "") or ""


@csrf_exempt
@require_http_methods(["POST"])
def translation_job_claim(request):
    """Claim the next untranslated Spanish sermon field for a worker."""
    authentication_error = _authenticate(request)
    if authentication_error:
        return authentication_error

    now = timezone.now()
    expires_at = now + timedelta(seconds=TRANSLATION_JOB_TTL_SECONDS)
    with transaction.atomic():
        TranslationJob.objects.filter(
            status=TranslationJob.Status.CLAIMED,
            expires_at__lte=now,
        ).update(status=TranslationJob.Status.EXPIRED)

        sermon_ids = Sermon.objects.order_by("sermon_date", "created_at").values_list(
            "pk", flat=True
        )
        for sermon_id in sermon_ids:
            sermon = Sermon.objects.select_for_update().get(pk=sermon_id)
            translation = SermonTranslation.objects.filter(
                sermon=sermon,
                language=SermonTranslation.Language.SPANISH,
            ).first()
            active_fields = set(
                TranslationJob.objects.filter(
                    sermon=sermon,
                    language=SermonTranslation.Language.SPANISH,
                    status=TranslationJob.Status.CLAIMED,
                    expires_at__gt=now,
                ).values_list("field", flat=True)
            )

            for field in TRANSLATION_FIELDS:
                source_text = _translation_source(sermon, field).strip()
                translated_text = getattr(translation, field, "") if translation else ""
                if not source_text or translated_text.strip() or field in active_fields:
                    continue

                raw_token = secrets.token_urlsafe(32)
                job = TranslationJob.objects.create(
                    sermon=sermon,
                    language=SermonTranslation.Language.SPANISH,
                    field=field,
                    source_text=source_text,
                    source_hash=hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
                    token_hash=make_password(raw_token),
                    expires_at=expires_at,
                )
                return JsonResponse(
                    {
                        "job_id": job.pk,
                        "job_token": raw_token,
                        "sermon_id": sermon.pk,
                        "sermon_title": sermon.title,
                        "source_language": "en",
                        "target_language": "es",
                        "field": field,
                        "source_text": source_text,
                        "source_hash": job.source_hash,
                        "expires_at": expires_at.isoformat(),
                    }
                )

    return JsonResponse(
        {"job": None, "message": "No untranslated Spanish sermon fields remain."}
    )


@csrf_exempt
@require_http_methods(["POST"])
def translation_job_submit(request, job_id):
    """Save one completed Spanish sermon field for a claimed translation job."""
    authentication_error = _authenticate(request)
    if authentication_error:
        return authentication_error

    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Request body must be valid JSON."}, status=400)

    job_token = str(payload.get("job_token", "")).strip()
    translation_text = payload.get("translation")
    if not job_token or not isinstance(translation_text, str) or not translation_text.strip():
        return JsonResponse(
            {"error": "job_token and a non-empty translation are required."},
            status=400,
        )

    with transaction.atomic():
        try:
            job = TranslationJob.objects.select_for_update().get(pk=job_id)
        except TranslationJob.DoesNotExist:
            return JsonResponse({"error": "Translation job not found."}, status=404)

        now = timezone.now()
        if not check_password(job_token, job.token_hash):
            return _unauthorized_response()
        if job.status != TranslationJob.Status.CLAIMED:
            return JsonResponse({"error": "Translation job is no longer active."}, status=409)
        if job.expires_at <= now:
            job.status = TranslationJob.Status.EXPIRED
            job.save(update_fields=("status",))
            return JsonResponse({"error": "Translation job has expired."}, status=410)

        current_source = _translation_source(job.sermon, job.field).strip()
        current_hash = hashlib.sha256(current_source.encode("utf-8")).hexdigest()
        if current_hash != job.source_hash:
            job.status = TranslationJob.Status.EXPIRED
            job.save(update_fields=("status",))
            return JsonResponse(
                {"error": "The English source changed; request a new translation job."},
                status=409,
            )

        translated, _ = SermonTranslation.objects.get_or_create(
            sermon=job.sermon,
            language=job.language,
        )
        setattr(translated, job.field, translation_text.strip())
        try:
            translated.full_clean()
        except ValidationError as error:
            return JsonResponse(
                {"error": "Translation validation failed.", "fields": error.message_dict},
                status=400,
            )
        translated.save()

        job.status = TranslationJob.Status.COMPLETED
        job.completed_at = now
        job.save(update_fields=("status", "completed_at"))

    return JsonResponse(
        {
            "message": "Translation saved.",
            "sermon_id": job.sermon_id,
            "field": job.field,
            "language": job.language,
        }
    )
