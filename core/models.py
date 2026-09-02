from django.core.exceptions import ValidationError
from django.db import models


class SiteSettings(models.Model):
    """Site-wide settings managed from the Django admin."""

    class Theme(models.TextChoices):
        DARK = "dark", "Dark"
        LIGHT = "light", "Light"
        MEDIUM = "medium", "Medium"

    DEFAULT_THEME = Theme.DARK

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
    theme = models.CharField(
        choices=Theme.choices,
        default=DEFAULT_THEME,
        help_text="Choose the visual theme for the entire public website.",
        max_length=10,
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

    def get_effective_theme(self):
        """Return a valid theme even if stored data is missing or invalid."""
        valid_themes = {theme.value for theme in self.Theme}
        if self.theme in valid_themes:
            return self.theme
        return self.DEFAULT_THEME

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


class AboutPage(models.Model):
    """Singleton configuration and metadata for the public About page."""

    title_en = models.CharField(max_length=200)
    title_es = models.CharField(blank=True, max_length=200)
    meta_description_en = models.TextField(max_length=320)
    meta_description_es = models.TextField(blank=True, max_length=320)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About page"
        verbose_name_plural = "About page"

    def save(self, *args, **kwargs):
        """Keep About content as one predictable database record."""
        self.pk = 1
        if type(self).objects.filter(pk=1).exists():
            kwargs["force_insert"] = False
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Keep the required About page record available for administrators."""
        raise ValueError("The About page cannot be deleted.")

    def __str__(self):
        return "About page"


class AboutSection(models.Model):
    """An ordered, bilingual content section on the About page."""

    KEY_CHOICES = (
        ("intro", "Introduction"),
        ("mission", "Mission"),
        ("beliefs", "Beliefs"),
        ("bilingual_ministry", "Bilingual ministry"),
        ("leadership", "Leadership"),
        ("visitor_cta", "Visitor call to action"),
    )

    page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name="sections",
    )
    key = models.CharField(choices=KEY_CHOICES, max_length=40)
    title_en = models.CharField(max_length=200)
    title_es = models.CharField(blank=True, max_length=200)
    body_en = models.TextField(blank=True)
    body_es = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("display_order", "key")
        constraints = (
            models.UniqueConstraint(
                fields=("page", "key"),
                name="unique_about_section_key",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    key__in=(
                        "intro",
                        "mission",
                        "beliefs",
                        "bilingual_ministry",
                        "leadership",
                        "visitor_cta",
                    )
                ),
                name="valid_about_section_key",
            ),
        )
        verbose_name = "About section"
        verbose_name_plural = "About sections"

    def __str__(self):
        return f"{self.page} - {self.get_key_display()}"


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
