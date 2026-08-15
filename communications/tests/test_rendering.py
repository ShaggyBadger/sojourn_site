from unittest.mock import Mock, patch

from django.test import TestCase, override_settings

from communications.models import EmailRecipient, EmailTemplate
from communications.rendering import TemplateRenderError, render_email_template


class EmailRenderingTests(TestCase):
    def setUp(self):
        self.recipient = EmailRecipient.objects.create(
            email="person@example.com",
            first_name="Ada",
        )
        self.template = EmailTemplate.objects.create(
            name="Weekly update",
            subject_template="Gathering on {{ meeting_date }}",
            greeting="Hello {{ first_name }},",
            standard_copy="Please join us.",
            closing="See you soon,\nSojourn Baptist Church",
        )

    @override_settings(PUBLIC_SITE_URL="https://example.com")
    def test_rendering_returns_html_text_and_unsubscribe_link(self):
        rendered = render_email_template(
            self.template,
            {
                "meeting_date": "Sunday",
                "meeting_time": "10:30 AM",
                "meeting_location": "123 Main St",
                "body": "Bring a friend.",
            },
            recipient=self.recipient,
        )

        self.assertEqual(rendered["subject"], "Gathering on Sunday")
        self.assertIn("Hello Ada,", rendered["html"])
        self.assertIn("Bring a friend.", rendered["html"])
        self.assertIn("https://example.com/subscribe/unsubscribe/", rendered["html"])
        self.assertIn("Bring a friend.", rendered["text"])

    def test_rendering_includes_sanitized_template_html_body(self):
        self.template.body_html = (
            "<h2>This week's update</h2>"
            "<p><strong>Join us</strong> for worship.</p>"
            '<p><a href="https://example.com">Learn more</a></p>'
            '<script>alert("not allowed")</script>'
            '<a href="javascript:alert(1)">Unsafe link</a>'
        )
        self.template.save(update_fields=("body_html", "updated_at"))

        rendered = render_email_template(
            self.template,
            {
                "meeting_date": "Sunday",
                "meeting_time": "10:30 AM",
                "meeting_location": "Church",
            },
            recipient=self.recipient,
            unsubscribe_url="https://example.com/unsubscribe/test/",
        )

        self.assertIn("<h2>This week&#x27;s update</h2>", rendered["html"])
        self.assertIn("<strong>Join us</strong>", rendered["html"])
        self.assertIn('href="https://example.com"', rendered["html"])
        self.assertNotIn("<script>", rendered["html"])
        self.assertNotIn("javascript:", rendered["html"])

    def test_rendering_escapes_user_values(self):
        rendered = render_email_template(
            self.template,
            {
                "meeting_date": "Sunday",
                "meeting_time": "10:30 AM",
                "meeting_location": "<script>alert(1)</script>",
            },
            recipient=self.recipient,
            unsubscribe_url="https://example.com/unsubscribe/test/",
        )

        self.assertNotIn("<script>", rendered["html"])
        self.assertIn("&lt;script&gt;", rendered["html"])

    @patch("communications.rendering.SiteSettings.objects.first")
    def test_rendering_includes_the_database_hero_image(self, get_site_settings):
        site_settings = Mock()
        site_settings.hero_image = Mock(
            url="https://objects.example.com/site/hero/church.jpg"
        )
        site_settings.hero_image_alt = "People worshiping together"
        get_site_settings.return_value = site_settings

        rendered = render_email_template(
            self.template,
            {
                "meeting_date": "Sunday",
                "meeting_time": "10:30 AM",
                "meeting_location": "Church",
            },
            recipient=self.recipient,
            unsubscribe_url="https://example.com/unsubscribe/test/",
        )

        self.assertIn(
            'src="https://objects.example.com/site/hero/church.jpg"',
            rendered["html"],
        )
        self.assertIn('alt="People worshiping together"', rendered["html"])

    def test_unknown_variables_are_rejected(self):
        self.template.subject_template = "Hello {{ password }}"
        self.template.save(update_fields=("subject_template", "updated_at"))

        with self.assertRaises(TemplateRenderError):
            render_email_template(
                self.template,
                {
                    "meeting_date": "Sunday",
                    "meeting_time": "10:30 AM",
                    "meeting_location": "Church",
                },
                recipient=self.recipient,
            )

    def test_required_context_is_enforced(self):
        with self.assertRaises(TemplateRenderError):
            render_email_template(
                self.template,
                {"meeting_date": "Sunday"},
                recipient=self.recipient,
            )
