from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from sermons.models import MAX_AUDIO_FILE_SIZE, Sermon, SermonCollection, validate_mp3


class SermonModelTests(TestCase):
    def test_collection_and_sermon_slugs_are_generated(self):
        collection = SermonCollection.objects.create(name="Genesis Saga")
        sermon = Sermon.objects.create(
            title="God's Promise",
            speaker="Pastor",
            sermon_date="2026-08-09",
            summary="A summary.",
            thesis="A thesis.",
            main_scripture="Genesis 12",
            media_file="sermons/audio/promise.mp3",
            collection=collection,
        )

        self.assertEqual(collection.slug, "genesis-saga")
        self.assertEqual(sermon.slug, "gods-promise")

    def test_published_sermon_requires_core_fields(self):
        sermon = Sermon(is_published=True)

        with self.assertRaises(ValidationError) as raised:
            sermon.full_clean()

        self.assertIn("title", raised.exception.message_dict)
        self.assertIn("media_file", raised.exception.message_dict)

    def test_mp3_validation_rejects_wrong_extension_and_large_files(self):
        not_mp3 = SimpleUploadedFile("sermon.wav", b"audio", content_type="audio/wav")
        with self.assertRaises(ValidationError):
            validate_mp3(not_mp3)

        class LargeUpload:
            name = "sermon.mp3"
            size = MAX_AUDIO_FILE_SIZE + 1
            content_type = "audio/mpeg"

        with self.assertRaises(ValidationError):
            validate_mp3(LargeUpload())

    def test_mp3_validation_accepts_stored_files_without_upload_metadata(self):
        class StoredFile:
            name = "sermon.mp3"
            size = 4

        validate_mp3(StoredFile())
