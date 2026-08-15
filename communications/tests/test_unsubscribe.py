from django.test import TestCase
from django.urls import reverse

from communications.models import EmailRecipient


class UnsubscribeViewTests(TestCase):
    def test_unsubscribe_requires_confirmation_then_marks_recipient(self):
        recipient = EmailRecipient.objects.create(email="person@example.com")
        url = reverse(
            "communications:unsubscribe",
            kwargs={"token": recipient.unsubscribe_token},
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Stop receiving church emails?")

        response = self.client.post(url)
        recipient.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have been unsubscribed.")
        self.assertEqual(recipient.status, EmailRecipient.Status.UNSUBSCRIBED)
        self.assertIsNotNone(recipient.unsubscribed_at)

    def test_unsubscribe_is_idempotent(self):
        recipient = EmailRecipient.objects.create(
            email="person@example.com",
            status=EmailRecipient.Status.UNSUBSCRIBED,
        )
        url = reverse(
            "communications:unsubscribe",
            kwargs={"token": recipient.unsubscribe_token},
        )

        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        recipient.refresh_from_db()
        self.assertEqual(recipient.status, EmailRecipient.Status.UNSUBSCRIBED)
