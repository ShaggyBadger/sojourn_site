from django.core.exceptions import ValidationError
from django.db import models


class SiteSettings(models.Model):
    """Site-wide settings managed from the Django admin."""

    hero_image = models.ImageField(
        blank=True,
        help_text="The image displayed in the homepage hero section.",
        upload_to="site/hero/",
    )
    hero_image_alt = models.CharField(
        blank=True,
        help_text="Describe the image for visitors using a screen reader.",
        max_length=255,
    )
    favicon = models.ImageField(
        blank=True,
        help_text="The small image shown in the browser tab.",
        upload_to="site/favicon/",
    )

    class Meta:
        verbose_name = "site settings"
        verbose_name_plural = "site settings"

    def clean(self):
        """Require alternative text whenever a hero image is selected."""
        if self.hero_image and not self.hero_image_alt.strip():
            raise ValidationError(
                {"hero_image_alt": "Add alternative text for the hero image."}
            )

    def save(self, *args, **kwargs):
        """Keep site settings as one predictable database record."""
        self.pk = 1
        if type(self).objects.filter(pk=1).exists():
            kwargs["force_insert"] = False
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Do not allow the required site-settings record to be deleted."""
        raise ValueError("Site settings cannot be deleted.")

    def __str__(self):
        return "Site settings"


class TeamMember(models.Model):
    """A pastor or ministry leader displayed in the homepage leadership section."""

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="Role in English.")
    role_es = models.CharField(
        blank=True,
        help_text="Spanish role, if different from the English role.",
        max_length=100,
    )
    bio = models.TextField(blank=True, help_text="Biography in English.")
    bio_es = models.TextField(blank=True, help_text="Biography in Spanish.")
    photo = models.ImageField(blank=True, upload_to="team/")
    photo_alt = models.CharField(
        blank=True,
        help_text="Describe the photo for visitors using a screen reader.",
        max_length=255,
    )
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "name")
        verbose_name = "team member"
        verbose_name_plural = "team members"

    def clean(self):
        """Require alternative text whenever a leadership photo is selected."""
        if self.photo and not self.photo_alt.strip():
            raise ValidationError({"photo_alt": "Add alternative text for the photo."})

    def __str__(self):
        return f"{self.name} - {self.role}"
