from django.db import transaction
from django.utils import timezone

from .models import EmailRecipient, RecipientGroup

PUBLIC_SIGNUP_GROUP = "Website Subscribers"


@transaction.atomic
def subscribe_recipient(*, email, first_name="", last_name=""):
    """Create or safely re-use a public website subscriber.

    Existing unsubscribed, bounced, and suppressed recipients are not
    reactivated by submitting the public form again.
    """
    recipient, created = EmailRecipient.objects.get_or_create(
        email=email,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "source": EmailRecipient.Source.WEBSITE_SIGNUP,
            "consent_at": timezone.now(),
        },
    )

    if recipient.status == EmailRecipient.Status.ACTIVE:
        group, _ = RecipientGroup.objects.get_or_create(
            name=PUBLIC_SIGNUP_GROUP,
            defaults={"description": "People who joined through the public website."},
        )
        group.members.add(recipient)

    return recipient, created
