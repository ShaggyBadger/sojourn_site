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
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Do not allow the required site-settings record to be deleted."""
        raise ValueError("Site settings cannot be deleted.")

    def __str__(self):
        return "Site settings"
