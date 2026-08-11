from django.test import TestCase

from core.models import SiteSettings


class HomePageTests(TestCase):
    def test_homepage_loads_without_site_settings(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hero image has been selected yet.")

    def test_site_settings_is_a_singleton(self):
        first_settings = SiteSettings.objects.create()
        second_settings = SiteSettings.objects.create()

        self.assertEqual(first_settings.pk, 1)
        self.assertEqual(second_settings.pk, 1)
        self.assertEqual(SiteSettings.objects.count(), 1)
