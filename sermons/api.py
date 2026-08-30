from datetime import date
import secrets

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import MAX_AUDIO_FILE_SIZE, Sermon, SermonCollection, SermonTag

MAX_REQUEST_BYTES = MAX_AUDIO_FILE_SIZE + (1024 * 1024)


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

    configured_key = getattr(settings, "SERMON_UPLOAD_API_KEY", "")
    token = _get_bearer_token(request)
    if not configured_key or not token:
        return _unauthorized_response()

    if not secrets.compare_digest(token, configured_key):
        return _unauthorized_response()

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
    if tag_slugs:
        tags = list(SermonTag.objects.filter(slug__in=tag_slugs))
        found_slugs = {tag.slug for tag in tags}
        unknown_slugs = [slug for slug in tag_slugs if slug not in found_slugs]
        if unknown_slugs:
            return JsonResponse(
                {"error": "Unknown tags.", "tags": unknown_slugs}, status=400
            )

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
