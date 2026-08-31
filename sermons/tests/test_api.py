import json
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from sermons.models import (
    Sermon,
    SermonCollection,
    SermonTag,
    SermonTranslation,
    TranslationJob,
)


@override_settings(
    SERMON_UPLOAD_API_KEY="test-upload-key",
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {"location": Path("/tmp/sojourn-sermon-api-tests")},
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    },
)
class SermonUploadApiTests(TestCase):
    def upload(self, **fields):
        fields.setdefault("title", "A New Sermon")
        fields.setdefault("speaker", "Pastor")
        fields.setdefault("sermon_date", "2026-08-30")
        fields.setdefault("summary", "A summary.")
        fields.setdefault("thesis", "A thesis.")
        fields.setdefault("main_scripture", "John 1")
        fields["media_file"] = SimpleUploadedFile(
            "sermon.mp3", b"audio", content_type="audio/mpeg"
        )
        return self.client.post(
            reverse("sermon_upload"),
            fields,
            HTTP_AUTHORIZATION="Bearer test-upload-key",
        )

    def test_missing_api_key_is_rejected(self):
        response = self.client.post(reverse("sermon_upload"))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Sermon.objects.count(), 0)

    def test_valid_upload_creates_unpublished_draft(self):
        response = self.upload(transcript="A transcript.")

        self.assertEqual(response.status_code, 201)
        payload = json.loads(response.content)
        sermon = Sermon.objects.get(pk=payload["id"])
        self.assertFalse(sermon.is_published)
        self.assertIsNone(sermon.published_at)
        self.assertEqual(sermon.slug, "a-new-sermon")
        self.assertEqual(sermon.transcript, "A transcript.")

    def test_upload_creates_missing_tags_and_assigns_existing_tags(self):
        existing_tag = SermonTag.objects.create(name="Worship")

        response = self.upload(tags="worship,new-life,new-life")

        self.assertEqual(response.status_code, 201)
        sermon = Sermon.objects.get(pk=response.json()["id"])
        self.assertEqual(
            set(sermon.tags.values_list("slug", flat=True)),
            {"worship", "new-life"},
        )
        self.assertEqual(SermonTag.objects.count(), 2)
        self.assertEqual(SermonTag.objects.get(slug="new-life").name, "New Life")
        self.assertEqual(sermon.tags.get(slug="worship"), existing_tag)

    def test_client_cannot_publish_through_upload_endpoint(self):
        response = self.upload(is_published="true")

        self.assertEqual(response.status_code, 201)
        self.assertFalse(Sermon.objects.get().is_published)

    def test_invalid_audio_is_rejected(self):
        response = self.client.post(
            reverse("sermon_upload"),
            {
                "title": "A New Sermon",
                "speaker": "Pastor",
                "sermon_date": "2026-08-30",
                "summary": "A summary.",
                "thesis": "A thesis.",
                "main_scripture": "John 1",
                "media_file": SimpleUploadedFile(
                    "sermon.wav", b"audio", content_type="audio/wav"
                ),
            },
            HTTP_AUTHORIZATION="Bearer test-upload-key",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Sermon.objects.count(), 0)

    def test_collections_require_the_api_key(self):
        SermonCollection.objects.create(name="Genesis")

        response = self.client.get("/api/v1/sermons/collections/")

        self.assertEqual(response.status_code, 401)

    def test_collections_return_names_and_slugs(self):
        collection = SermonCollection.objects.create(
            name="The Gospel of John", description="A series through John."
        )

        response = self.client.get(
            "/api/v1/sermons/collections/",
            HTTP_AUTHORIZATION="Bearer test-upload-key",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "collections": [
                    {
                        "id": collection.pk,
                        "name": "The Gospel of John",
                        "slug": "the-gospel-of-john",
                        "description": "A series through John.",
                        "is_published": True,
                    }
                ]
            },
        )

    def test_claim_returns_next_missing_translation_field(self):
        sermon = Sermon.objects.create(
            title="A New Sermon",
            speaker="Pastor",
            sermon_date="2026-08-30",
            summary="A summary.",
            thesis="A thesis.",
            main_scripture="John 1",
            media_file="sermons/audio/sermon.mp3",
        )

        response = self.client.post(
            reverse("translation_job_claim"),
            HTTP_AUTHORIZATION="Bearer test-upload-key",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["sermon_id"], sermon.pk)
        self.assertEqual(payload["field"], "title")
        self.assertEqual(payload["source_text"], "A New Sermon")
        self.assertTrue(
            TranslationJob.objects.filter(
                pk=payload["job_id"], status=TranslationJob.Status.CLAIMED
            ).exists()
        )

    def test_submit_saves_translation_and_completes_job(self):
        sermon = Sermon.objects.create(
            title="A New Sermon",
            speaker="Pastor",
            sermon_date="2026-08-30",
            summary="A summary.",
            thesis="A thesis.",
            main_scripture="John 1",
            media_file="sermons/audio/sermon.mp3",
        )
        claim = self.client.post(
            reverse("translation_job_claim"),
            HTTP_AUTHORIZATION="Bearer test-upload-key",
        )
        job = claim.json()

        response = self.client.post(
            reverse("translation_job_submit", kwargs={"job_id": job["job_id"]}),
            data=json.dumps(
                {
                    "job_token": job["job_token"],
                    "translation": "Un Sermón Nuevo",
                }
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION="Bearer test-upload-key",
        )

        self.assertEqual(response.status_code, 200)
        translation = SermonTranslation.objects.get(sermon=sermon, language="es")
        self.assertEqual(translation.title, "Un Sermón Nuevo")
        self.assertEqual(
            TranslationJob.objects.get(pk=job["job_id"]).status,
            TranslationJob.Status.COMPLETED,
        )

    def test_submit_with_wrong_job_token_is_rejected(self):
        Sermon.objects.create(
            title="A New Sermon",
            speaker="Pastor",
            sermon_date="2026-08-30",
            summary="A summary.",
            thesis="A thesis.",
            main_scripture="John 1",
            media_file="sermons/audio/sermon.mp3",
        )
        claim = self.client.post(
            reverse("translation_job_claim"),
            HTTP_AUTHORIZATION="Bearer test-upload-key",
        )

        response = self.client.post(
            reverse(
                "translation_job_submit", kwargs={"job_id": claim.json()["job_id"]}
            ),
            data=json.dumps(
                {"job_token": "wrong-token", "translation": "Traducción"}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION="Bearer test-upload-key",
        )

        self.assertEqual(response.status_code, 401)
