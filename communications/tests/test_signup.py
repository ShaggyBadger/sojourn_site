from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from communications.models import EmailRecipient, RecipientGroup
from communications.services import PUBLIC_SIGNUP_GROUP


class SubscribeViewTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_signup_page_loads_with_csrf_token(self):
        response = self.client.get(reverse("communications:subscribe"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "communications/subscribe.html")
        self.assertContains(response, 'name="csrfmiddlewaretoken"')

    def test_signup_page_renders_spanish_interface_text(self):
        self.client.cookies["django_language"] = "es"

        response = self.client.get(reverse("communications:subscribe"))

        self.assertContains(response, "Mantente conectado")
        self.assertContains(response, "Dirección de correo electrónico")
        self.assertContains(response, "Suscribirme")
        self.assertContains(response, "Iglesia Sojourn")

    def test_valid_signup_creates_recipient_and_group(self):
        response = self.client.post(
            reverse("communications:subscribe"),
            {
                "email": "  Person@Example.COM ",
                "first_name": "Ada",
                "last_name": "Lovelace",
                "consent": "on",
                "website": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are on the list.")
        recipient = EmailRecipient.objects.get()
        self.assertEqual(recipient.email, "person@example.com")
        self.assertEqual(recipient.source, EmailRecipient.Source.WEBSITE_SIGNUP)
        self.assertIsNotNone(recipient.consent_at)
        group = RecipientGroup.objects.get(name=PUBLIC_SIGNUP_GROUP)
        self.assertSequenceEqual(list(group.members.all()), [recipient])

    def test_duplicate_signup_does_not_reveal_existing_membership(self):
        EmailRecipient.objects.create(email="person@example.com")

        response = self.client.post(
            reverse("communications:subscribe"),
            {"email": "PERSON@example.com", "consent": "on", "website": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This email is already on our list.")
        self.assertEqual(EmailRecipient.objects.count(), 1)

    def test_invalid_signup_does_not_create_recipient(self):
        response = self.client.post(
            reverse("communications:subscribe"),
            {"email": "not-an-email", "consent": "on", "website": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid email address.")
        self.assertEqual(EmailRecipient.objects.count(), 0)

    def test_honeypot_submission_is_accepted_without_creating_recipient(self):
        response = self.client.post(
            reverse("communications:subscribe"),
            {
                "email": "bot@example.com",
                "consent": "on",
                "website": "bot filled this",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are on the list.")
        self.assertEqual(EmailRecipient.objects.count(), 0)

    def test_signup_is_throttled_after_five_submissions_per_address(self):
        url = reverse("communications:subscribe")
        for number in range(5):
            self.client.post(
                url,
                {
                    "email": f"person{number}@example.com",
                    "consent": "on",
                    "website": "",
                },
            )

        self.client.post(
            url,
            {"email": "person5@example.com", "consent": "on", "website": ""},
        )

        self.assertEqual(EmailRecipient.objects.count(), 5)
