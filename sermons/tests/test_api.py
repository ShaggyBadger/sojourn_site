import json
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from sermons.models import Sermon, SermonCollection


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
