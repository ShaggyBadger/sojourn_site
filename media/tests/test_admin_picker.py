from io import BytesIO

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from media.models import MediaAsset, MediaTag


def image_upload(name):
    output = BytesIO()
    Image.new("RGB", (32, 32), (197, 168, 128)).save(output, format="PNG")
    return SimpleUploadedFile(name, output.getvalue(), content_type="image/png")


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {"location": "/tmp/sojourn-media-picker-tests"},
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
class MediaPickerAdminTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="test-password",
        )
        self.client.force_login(self.user)

    def test_picker_filters_assets_by_tag_and_shows_preview(self):
        icon_tag = MediaTag.objects.create(name="Homepage icon")
        matching = MediaAsset.objects.create(file=image_upload("matching.png"), name="Matching")
        matching.tags.add(icon_tag)
        other = MediaAsset.objects.create(file=image_upload("other.png"), name="Other")

        response = self.client.get(
            reverse("admin:media_mediaasset_picker"),
            {"field_id": "id_homepage_icon_1_asset", "tag": icon_tag.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Matching")
        self.assertNotContains(response, "Other")
        self.assertContains(response, matching.file.url, html=False)
        self.assertContains(response, "id_homepage_icon_1_asset", html=False)
