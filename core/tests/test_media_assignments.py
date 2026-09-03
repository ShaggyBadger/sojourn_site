from io import BytesIO

from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from core.models import SiteSettings
from media.models import MediaAsset


def image_upload(name, image_format="PNG", size=(32, 32)):
    output = BytesIO()
    Image.new("RGB", size, (197, 168, 128)).save(output, format=image_format)
    content_types = {"JPEG": "image/jpeg", "PNG": "image/png"}
    return SimpleUploadedFile(
        name, output.getvalue(), content_type=content_types[image_format]
    )


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {"location": "/tmp/sojourn-media-assignment-tests"},
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
class MediaAssignmentTests(TestCase):
    def test_non_square_favicon_is_automatically_prepared(self):
        source = MediaAsset.objects.create(
            file=image_upload("favicon-source.jpg", "JPEG", (240, 120)),
            name="Favicon source",
        )

        settings = SiteSettings.objects.create(favicon_asset=source)
        settings.refresh_from_db()

        self.assertNotEqual(settings.favicon_asset_id, source.pk)
        self.assertEqual(settings.favicon_asset.mime_type, "image/png")
        self.assertEqual(settings.favicon_asset.width, 512)
        self.assertEqual(settings.favicon_asset.height, 512)
        self.assertEqual(source.width, 240)
        self.assertEqual(source.height, 120)

    def test_homepage_uses_selected_assets_for_hero_favicon_and_icons(self):
        hero = MediaAsset.objects.create(file=image_upload("hero.png"), name="Hero")
        favicon = MediaAsset.objects.create(
            file=image_upload("favicon.png"), name="Favicon"
        )
        icons = [
            MediaAsset.objects.create(file=image_upload(f"icon-{number}.png"), name=f"Icon {number}")
            for number in range(1, 8)
        ]
        SiteSettings.objects.create(
            hero_image_asset=hero,
            favicon_asset=favicon,
            hero_image_alt_en="People worshiping together",
            **{
                f"homepage_statement_{number}_en": statement
                for number, statement in enumerate(
                    (
                        "Centered on God",
                        "On Mission Together",
                        "Dependent on God",
                        "Journeying Homeward",
                        "Driven by the Word",
                        "In Supernatural Community",
                        "Made Holy by Grace",
                    ),
                    start=1,
                )
            },
            **{
                f"homepage_icon_{number}_asset": asset
                for number, asset in enumerate(icons, start=1)
            },
        )

        response = self.client.get("/")

        self.assertContains(response, hero.file.url, html=False)
        self.assertContains(response, favicon.file.url, html=False)
        self.assertContains(response, "Centered on God")
        self.assertContains(response, "Made Holy by Grace")

    def test_homepage_hides_icon_section_until_all_assets_are_selected(self):
        asset = MediaAsset.objects.create(file=image_upload("icon.png"), name="Icon")
        SiteSettings.objects.create(homepage_icon_1_asset=asset)

        response = self.client.get("/")

        self.assertNotContains(response, "Centered on God")
