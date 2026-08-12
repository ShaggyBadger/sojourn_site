from django.test import TestCase

from core.models import SiteSettings, TeamMember


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

    def test_homepage_displays_published_team_members_in_order(self):
        TeamMember.objects.create(name="Second", role="Pastor", order=2)
        TeamMember.objects.create(name="First", role="Pastor", order=1)
        TeamMember.objects.create(
            name="Hidden", role="Pastor", order=0, is_published=False
        )

        response = self.client.get("/")

        self.assertContains(response, "First")
        self.assertContains(response, "Second")
        self.assertNotContains(response, "Hidden")
        self.assertLess(response.content.index(b"First"), response.content.index(b"Second"))
