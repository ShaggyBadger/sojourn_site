from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from communications.models import EmailTemplate


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class TemplatePreviewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="staff",
            password="test-password",
            is_staff=True,
        )
        self.client.force_login(self.user)
        self.template = EmailTemplate.objects.create(name="Weekly update")
        self.url = reverse(
            "communications:template-preview",
            kwargs={"template_id": self.template.pk},
        )

    def test_non_staff_cannot_open_preview(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_staff_can_preview_and_send_test_email(self):
        response = self.client.post(
            self.url,
            {
                "meeting_date": "Sunday",
                "meeting_time": "10:30 AM",
                "meeting_location": "Church",
                "first_name": "Friend",
                "body": "Announcements",
                "notes": "",
                "test_email": "test@example.com",
                "send_test": "1",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rendered email")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["test@example.com"])
        self.assertEqual(len(mail.outbox[0].alternatives), 1)
