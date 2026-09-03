from io import BytesIO
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from media.models import MediaAsset, MediaTag, normalize_tag_name
from media.validators import validate_image_upload


def image_upload(name="church-photo.jpg", image_format="JPEG", size=(120, 80)):
    output = BytesIO()
    image = Image.new("RGB", size, (197, 168, 128))
    image.save(output, format=image_format)
    content_types = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}
    return SimpleUploadedFile(name, output.getvalue(), content_type=content_types[image_format])


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {"location": "/tmp/sojourn-media-tests"},
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
class MediaAssetTests(TestCase):
    def test_valid_upload_records_metadata_and_uses_dedicated_path(self):
        asset = MediaAsset.objects.create(
            file=image_upload(),
            name="Church photo",
            alt_text_en="People worshiping together",
        )

        self.assertEqual(asset.original_filename, "church-photo.jpg")
        self.assertEqual(asset.mime_type, "image/jpeg")
        self.assertEqual(asset.width, 120)
        self.assertEqual(asset.height, 80)
        self.assertEqual(asset.storage_status, MediaAsset.StorageStatus.PRESENT)
        self.assertTrue(asset.file.name.startswith("media/assets/"))
        self.assertEqual(len(asset.sha256), 64)

    def test_invalid_uploads_are_rejected(self):
        invalid = SimpleUploadedFile("page.html", b"<html>", content_type="text/html")

        with self.assertRaises(ValidationError):
            validate_image_upload(invalid)

    def test_tags_are_normalized_and_database_unique(self):
        self.assertEqual(normalize_tag_name("  Home  PAGE "), "home page")
        first = MediaTag.objects.create(name=" Homepage ")

        self.assertEqual(first.name, "Homepage")
        self.assertEqual(first.normalized_name, "homepage")
        with self.assertRaises(ValidationError):
            MediaTag(name="homepage").full_clean()

    def test_replacing_an_asset_uses_a_new_storage_key(self):
        asset = MediaAsset.objects.create(file=image_upload(), name="Church photo")
        old_name = asset.file.name

        asset.file = image_upload("replacement.png", "PNG")
        asset.save()
        asset.refresh_from_db()

        self.assertNotEqual(asset.file.name, old_name)
        self.assertFalse(asset.file.storage.exists(old_name))

    def test_missing_required_name_is_rejected(self):
        with self.assertRaises(ValidationError):
            MediaAsset.objects.create(file=image_upload(), name="")
