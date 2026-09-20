from django.db import IntegrityError
from django.test import TestCase

from core.admin import SiteSettingsAdmin
from core.models import AboutPage, AboutSection, SiteSettings, TeamMember
from core.selectors import get_localized_about_content
from sermons.models import Sermon


class HomePageTests(TestCase):
    def test_homepage_loads_without_site_settings(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hero image has been selected yet.")

    def test_admin_path_reaches_django_admin(self):
        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_homepage_displays_hero_message(self):
        response = self.client.get("/")

        self.assertContains(response, "Delighting in God")
        self.assertContains(response, "and helping others to do the same")

    def test_homepage_declares_a_phone_bookmark_icon(self):
        response = self.client.get("/")

        self.assertContains(response, 'rel="apple-touch-icon"', html=False)

    def test_homepage_renders_spanish_hero(self):
        self.client.cookies["django_language"] = "es"
        response = self.client.get("/")

        self.assertContains(response, "Deleitándonos en Dios")

    def test_site_settings_is_a_singleton(self):
        first_settings = SiteSettings.objects.create()
        second_settings = SiteSettings.objects.create()

        self.assertEqual(first_settings.pk, 1)
        self.assertEqual(second_settings.pk, 1)
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_site_settings_defaults_to_dark_theme(self):
        site_settings = SiteSettings.objects.create()

        self.assertEqual(site_settings.theme, SiteSettings.Theme.DARK)
        self.assertEqual(site_settings.get_effective_theme(), "dark")

    def test_homepage_distinctives_have_eight_slots(self):
        site_settings = SiteSettings.objects.create()

        self.assertEqual(len(site_settings.get_homepage_icons()), 8)
        self.assertEqual(len(site_settings.get_homepage_statements()), 8)

    def test_selected_theme_is_rendered_on_public_document(self):
        SiteSettings.objects.create(theme=SiteSettings.Theme.LIGHT)

        response = self.client.get("/")

        self.assertContains(response, '<html lang="en" data-theme="light">', html=False)

    def test_workshop_theme_is_rendered_on_public_document(self):
        SiteSettings.objects.create(theme=SiteSettings.Theme.WORKSHOP)

        response = self.client.get("/")

        self.assertContains(response, '<html lang="en" data-theme="workshop">', html=False)

    def test_invalid_stored_theme_falls_back_to_dark(self):
        SiteSettings.objects.create(theme="not-a-theme")

        response = self.client.get("/")

        self.assertContains(response, '<html lang="en" data-theme="dark">', html=False)

    def test_site_settings_admin_exposes_theme_in_appearance_fieldset(self):
        fields = dict(SiteSettingsAdmin.fieldsets)

        self.assertEqual(fields["Appearance"]["fields"], ("theme",))

    def test_homepage_does_not_display_team_members(self):
        TeamMember.objects.create(name="Second", role="Pastor", order=2)
        TeamMember.objects.create(name="First", role="Pastor", order=1)
        TeamMember.objects.create(
            name="Hidden", role="Pastor", order=0, is_published=False
        )

        response = self.client.get("/")

        self.assertNotContains(response, "First")
        self.assertNotContains(response, "Second")
        self.assertNotContains(response, "Hidden")

    def test_homepage_links_to_latest_published_sermon_by_sermon_date(self):
        Sermon.objects.create(
            title="Older Message",
            speaker="Pastor",
            sermon_date="2026-08-01",
            summary="Summary",
            thesis="Thesis",
            main_scripture="John 1",
            media_file="sermons/audio/older.mp3",
            is_published=True,
        )
        latest = Sermon.objects.create(
            title="Latest Message",
            speaker="Pastor",
            sermon_date="2026-08-10",
            summary="Summary",
            thesis="Thesis",
            main_scripture="John 2",
            media_file="sermons/audio/latest.mp3",
            is_published=True,
        )
        Sermon.objects.create(
            title="Future Message",
            speaker="Pastor",
            sermon_date="2099-01-01",
            summary="Summary",
            thesis="Thesis",
            main_scripture="John 3",
            media_file="sermons/audio/future.mp3",
            is_published=True,
        )

        response = self.client.get("/")

        self.assertContains(response, "Latest Message")
        self.assertContains(response, f'href="/sermons/{latest.slug}/"', html=False)
        self.assertNotContains(response, "Older Message")
        self.assertNotContains(response, "Future Message")

    def test_homepage_new_here_card_links_to_visitor_page(self):
        response = self.client.get("/")

        self.assertContains(response, 'href="/new-here/"', html=False)


class NewHerePageTests(TestCase):
    def test_new_here_page_loads_with_practical_visitor_information(self):
        response = self.client.get("/new-here/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "new_here.html")
        self.assertContains(response, "Sunday gathering")
        self.assertContains(response, "10:30 AM")
        self.assertContains(response, "Reflective worship and faithful teaching")
        self.assertContains(response, "Business casual")

    def test_new_here_page_renders_spanish_translation(self):
        self.client.cookies["django_language"] = "es"
        response = self.client.get("/new-here/")

        self.assertContains(response, "Una iglesia bilingüe para nuestros vecinos")
        self.assertContains(response, "Reunión del domingo")


class GivingPageTests(TestCase):
    def test_giving_page_links_to_zeffy(self):
        response = self.client.get("/giving/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "https://www.zeffy.com/en-US/donation-form/tithegive-to-sojourn-church",
        )
        self.assertContains(response, "Give through Zeffy")

    def test_homepage_give_card_links_to_partner_page(self):
        response = self.client.get("/")

        self.assertContains(response, 'href="/partner-with-us/"', html=False)
        self.assertContains(response, "Partner with us")
        self.assertContains(response, "Join us through prayer, generosity, presence, and service")

    def test_subscribe_path_reaches_communications_app(self):
        response = self.client.get("/subscribe/")

        self.assertNotEqual(response.status_code, 404)

    def test_giving_page_renders_spanish_translation(self):
        self.client.cookies["django_language"] = "es"
        response = self.client.get("/giving/")

        self.assertContains(response, "Usa nuestro formulario para dar en línea")


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
        AboutSection.objects.filter(page=page, key="beliefs").update(is_visible=False)

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
        self.assertContains(response, "About Sojourn Church")
        self.assertContains(response, "A church for our neighbors")
        self.assertContains(response, "Apostles' Creed")
        self.assertContains(response, "Nicene Creed")
        self.assertContains(response, "Baptist Faith and Message 2000")
        self.assertContains(response, "New Hampshire Confession of Faith")
        self.assertNotContains(response, "London Baptist Confession")
        self.assertNotContains(response, "As a Baptist church")

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
        self.assertContains(response, "Acerca de Iglesia Sojourn")
        self.assertContains(response, "Una iglesia para nuestros vecinos")
        self.assertContains(response, "Credo de los Apóstoles")
        self.assertContains(response, "Credo Niceno")
        self.assertContains(response, "Fe y Mensaje Bautistas 2000")
        self.assertContains(response, "Confesión de Fe de New Hampshire")
        self.assertNotContains(response, "Confesión Bautista de Fe de Londres")

    def test_about_page_links_to_the_beliefs_hub(self):
        response = self.client.get("/about/")

        self.assertContains(response, 'href="/what-we-believe/"', html=False)
        self.assertContains(response, "What We Believe")
        self.assertContains(response, 'href="/apostles-creed/"', html=False)
        self.assertContains(response, 'href="/nicene-creed/"', html=False)
        self.assertContains(response, 'href="/baptist-faith-and-message-2000/"', html=False)
        self.assertContains(response, 'href="/new-hampshire-confession-of-faith/"', html=False)


class HowWeAreLedPageTests(TestCase):
    def test_how_we_are_led_page_renders_the_three_leadership_convictions(self):
        response = self.client.get("/how-we-are-led/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "how_we_are_led.html")
        self.assertContains(response, "How We Are Led")
        self.assertContains(response, "Elder-Led")
        self.assertContains(response, "Deacon-Served")
        self.assertContains(response, "Congregationally-Ruled")
        self.assertContains(response, 'rel="canonical"', html=False)

    def test_how_we_are_led_page_renders_spanish_content(self):
        self.client.cookies["django_language"] = "es"
        response = self.client.get("/how-we-are-led/")

        self.assertContains(response, "Cómo somos guiados")
        self.assertContains(response, "Guiada por ancianos")
        self.assertContains(response, "Servida por diáconos")
        self.assertContains(response, "Gobernada por la congregación")

    def test_how_we_are_led_page_is_in_sitemap(self):
        response = self.client.get("/sitemap.xml")

        self.assertContains(response, "/how-we-are-led/")


class PartnerWithUsPageTests(TestCase):
    def test_partner_page_renders_all_four_paths(self):
        response = self.client.get("/partner-with-us/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "partner_with_us.html")
        self.assertContains(response, "Partner With Us")
        self.assertContains(response, "Connect")
        self.assertContains(response, "Pray")
        self.assertContains(response, "Give")
        self.assertContains(response, "Go")
        self.assertContains(response, 'href="/giving/"', html=False)
        self.assertContains(response, 'href="/subscribe/"', html=False)
        self.assertContains(response, 'href="/subscribe/planting-interest/"', html=False)

    def test_partner_page_renders_spanish_content(self):
        self.client.cookies["django_language"] = "es"
        response = self.client.get("/partner-with-us/")

        self.assertContains(response, "Colabora con nosotros")
        self.assertContains(response, "Conecta")
        self.assertContains(response, "Ora")
        self.assertContains(response, "Da")
        self.assertContains(response, "Ve")

    def test_partner_page_is_in_sitemap(self):
        response = self.client.get("/sitemap.xml")

        self.assertContains(response, "/partner-with-us/")


class ConfessionPageTests(TestCase):
    def test_confession_page_loads_with_all_articles_and_metadata(self):
        response = self.client.get("/new-hampshire-confession-of-faith/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "confession.html")
        self.assertContains(response, "New Hampshire Confession of Faith")
        self.assertContains(response, "I. Of the Scriptures")
        self.assertContains(response, "XVIII. Of the World to Come")
        self.assertContains(response, "og:type", html=False)
        self.assertContains(response, "truegraceofgod.org/1853-new-hampshire-confession/")

    def test_confession_page_renders_spanish_interface(self):
        self.client.cookies["django_language"] = "es"
        response = self.client.get("/new-hampshire-confession-of-faith/")

        self.assertContains(response, '<html lang="es">', html=False)
        self.assertContains(response, "Confesión de Fe de New Hampshire")
        self.assertContains(response, "Contenido de la confesión")
        self.assertContains(response, "De las Escrituras")
        self.assertContains(response, "Del Mundo Venidero")
        self.assertNotContains(response, "Of the Scriptures")


class BeliefsPageTests(TestCase):
    def test_beliefs_hub_links_to_each_statement(self):
        response = self.client.get("/what-we-believe/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "beliefs.html")
        self.assertContains(response, "What We Believe")
        self.assertContains(response, 'href="/nicene-creed/"', html=False)
        self.assertContains(response, 'href="/apostles-creed/"', html=False)
        self.assertContains(
            response,
            'href="/baptist-faith-and-message-2000/"',
            html=False,
        )
        self.assertContains(
            response,
            'href="/new-hampshire-confession-of-faith/"',
            html=False,
        )

    def test_dedicated_creed_pages_have_unique_metadata(self):
        response = self.client.get("/nicene-creed/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "belief_detail.html")
        self.assertContains(response, "Nicene Creed")
        self.assertNotContains(response, "confession-navigation")
        self.assertContains(response, "confession-document")
        self.assertContains(response, "confession-prose")
        self.assertContains(response, "confession-source")
        self.assertContains(response, "og:title", html=False)
        self.assertContains(response, 'rel="canonical"', html=False)

    def test_baptist_faith_page_links_to_official_statement(self):
        response = self.client.get("/baptist-faith-and-message-2000/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Baptist Faith and Message 2000")
        self.assertContains(response, "XVIII. The Family")
        self.assertContains(response, "original overview of all 18 articles")
        self.assertContains(response, "https://bfm.sbc.net/")
        self.assertContains(response, "belief-context-callout")

    def test_baptist_faith_page_uses_official_spanish_statement_link(self):
        self.client.cookies["django_language"] = "es"
        response = self.client.get("/baptist-faith-and-message-2000/")

        self.assertContains(response, "XVIII. La Familia")
        self.assertContains(response, "resumen original de Sojourn")
        self.assertContains(response, "bfandm.wpengine.com/es/fe-y-mensaje-bautistas/")

    def test_beliefs_pages_render_spanish_content(self):
        self.client.cookies["django_language"] = "es"
        response = self.client.get("/what-we-believe/")

        self.assertContains(response, '<html lang="es">', html=False)
        self.assertContains(response, "Lo que creemos")
        self.assertContains(response, "Credo Niceno")

    def test_beliefs_are_in_sitemap(self):
        response = self.client.get("/sitemap.xml")

        self.assertContains(response, "/what-we-believe/")
        self.assertContains(response, "/nicene-creed/")
        self.assertContains(response, "/apostles-creed/")
