import uuid

from django.conf import settings
from django.db import models


class EmailRecipient(models.Model):
    """A person staff may select for church email communications."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        UNSUBSCRIBED = "unsubscribed", "Unsubscribed"
        BOUNCED = "bounced", "Bounced"
        SUPPRESSED = "suppressed", "Suppressed"

    class Source(models.TextChoices):
        ADMIN = "admin", "Admin"
        IMPORT = "import", "Import"
        WEBSITE_SIGNUP = "website_signup", "Website signup"
        PROVIDER = "provider", "Provider"
        OTHER = "other", "Other"

    email = models.EmailField(unique=True)
    unsubscribe_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    first_name = models.CharField(blank=True, max_length=100)
    last_name = models.CharField(blank=True, max_length=100)
    status = models.CharField(
        choices=Status.choices,
        default=Status.ACTIVE,
        max_length=20,
    )
    source = models.CharField(
        choices=Source.choices,
        default=Source.ADMIN,
        max_length=20,
    )
    consent_at = models.DateTimeField(blank=True, null=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("last_name", "first_name", "email")
        verbose_name = "email recipient"
        verbose_name_plural = "email recipients"

    def save(self, *args, **kwargs):
        """Normalize addresses before enforcing the database uniqueness rule."""
        self.email = self.email.strip().casefold()
        super().save(*args, **kwargs)

    def __str__(self):
        name = " ".join(part for part in (self.first_name, self.last_name) if part)
        return f"{name} <{self.email}>" if name else self.email


class EmailTemplate(models.Model):
    """Reusable content settings for a controlled email layout."""

    class Layout(models.TextChoices):
        WEEKLY_MEETING = "weekly_meeting", "Weekly meeting"

    class Language(models.TextChoices):
        ENGLISH = "en", "English"
        SPANISH = "es", "Spanish"
        BILINGUAL = "bilingual", "Bilingual"

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    layout = models.CharField(
        choices=Layout.choices,
        default=Layout.WEEKLY_MEETING,
        max_length=30,
    )
    subject_template = models.CharField(
        default="This week's gathering - {{ meeting_date }}",
        max_length=255,
    )
    greeting = models.CharField(default="Hello {{ first_name }},", max_length=255)
    standard_copy = models.TextField(blank=True)
    body_html = models.TextField(
        blank=True,
        help_text=(
            "Optional safe HTML for the main message body. "
            "Use paragraphs, headings, lists, links, strong, and emphasis."
        ),
    )
    closing = models.TextField(
        default="We hope to see you there,\nSojourn Baptist Church"
    )
    language = models.CharField(
        choices=Language.choices,
        default=Language.ENGLISH,
        max_length=10,
    )
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="email_templates_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "email template"
        verbose_name_plural = "email templates"

    def __str__(self):
        return self.name


class RecipientGroup(models.Model):
    """A manually maintained audience of email recipients."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(
        EmailRecipient,
        related_name="groups",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "recipient group"
        verbose_name_plural = "recipient groups"

    def __str__(self):
        return self.name
