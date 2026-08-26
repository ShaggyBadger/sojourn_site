from django.test import TestCase

from communications.models import EmailRecipient, RecipientGroup


class EmailRecipientTests(TestCase):
    def test_email_is_normalized_when_saved(self):
        recipient = EmailRecipient.objects.create(email="  Person@Example.COM ")

        self.assertEqual(recipient.email, "person@example.com")

    def test_names_are_optional(self):
        recipient = EmailRecipient.objects.create(email="person@example.com")

        self.assertEqual(str(recipient), "person@example.com")

    def test_name_is_used_in_display(self):
        recipient = EmailRecipient.objects.create(
            email="person@example.com",
            first_name="Ada",
            last_name="Lovelace",
        )

        self.assertEqual(str(recipient), "Ada Lovelace <person@example.com>")


class RecipientGroupTests(TestCase):
    def test_group_members_are_unique(self):
        recipient = EmailRecipient.objects.create(email="person@example.com")
        group = RecipientGroup.objects.create(name="Sunday Updates")

        group.members.add(recipient, recipient)

        self.assertEqual(group.members.count(), 1)
