from django.db import IntegrityError
from django.test import TestCase

from core.models import AboutPage, AboutSection, SiteSettings, TeamMember
from core.selectors import get_localized_about_content


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
        self.assertLess(
            response.content.index(b"First"), response.content.index(b"Second")
        )


class AboutPageTests(TestCase):
    def test_about_page_is_a_singleton(self):
        page = AboutPage.objects.get(pk=1)
        AboutPage.objects.create(
            title_en="Replacement",
            meta_description_en="Replacement description",
        )

        page.refresh_from_db()

        self.assertEqual(page.pk, 1)
        self.assertEqual(AboutPage.objects.count(), 1)

    def test_about_sections_have_unique_keys_per_page(self):
        page = AboutPage.objects.get(pk=1)

        with self.assertRaises(IntegrityError):
            AboutSection.objects.create(
                page=page,
                key="mission",
                title_en="Duplicate mission",
            )

    def test_about_page_uses_database_content_and_section_visibility(self):
        page = AboutPage.objects.get(pk=1)
        page.title_en = "Our Story"
        page.save()
        AboutSection.objects.filter(page=page, key="mission").update(
            title_en="A shared mission",
            body_en="Edited mission content.",
        )
        AboutSection.objects.filter(page=page, key="beliefs").update(
            is_visible=False
        )

        response = self.client.get("/about/")

        self.assertContains(response, "Our Story")
        self.assertContains(response, "A shared mission")
        self.assertContains(response, "Edited mission content.")
        self.assertNotContains(response, "Rooted in the historic Christian faith")

    def test_spanish_content_falls_back_and_reports_missing_fields(self):
        page = AboutPage.objects.get(pk=1)
        page.title_es = ""
        page.save()
        AboutSection.objects.filter(page=page, key="mission").update(
            title_es="",
            body_es="",
        )

        content = get_localized_about_content("es")

        self.assertIn("page:title", content.fallback_keys)
        self.assertIn("section:mission:title", content.fallback_keys)
        self.assertIn("section:mission:body", content.fallback_keys)

    def test_about_page_loads_with_core_content(self):
        response = self.client.get("/about/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")
        self.assertContains(response, "A church for our neighbors")
        self.assertContains(response, "We affirm the historic Christian faith")

    def test_about_page_uses_published_team_members_in_order(self):
        TeamMember.objects.create(name="Second", role="Pastor", order=2)
        TeamMember.objects.create(name="First", role="Pastor", order=1)
        TeamMember.objects.create(
            name="Hidden", role="Pastor", order=0, is_published=False
        )

        response = self.client.get("/about/")

        self.assertContains(response, "First")
        self.assertContains(response, "Second")
        self.assertNotContains(response, "Hidden")
        self.assertLess(
            response.content.index(b"First"), response.content.index(b"Second")
        )

    def test_about_page_omits_empty_leadership_section(self):
        response = self.client.get("/about/")

        self.assertNotContains(response, "Pastoral leadership")
        self.assertNotContains(response, "about-pastor-card")

    def test_about_page_renders_spanish_translation(self):
        self.client.cookies["django_language"] = "es"
        response = self.client.get("/about/")

        self.assertContains(response, '<html lang="es">', html=False)
        self.assertContains(response, "Acerca de la Iglesia Bautista Sojourn")
        self.assertContains(response, "Una iglesia para nuestros vecinos")
        self.assertContains(response, "Arraigados en la fe cristiana histórica")
