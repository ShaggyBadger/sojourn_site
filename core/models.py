from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .favicon import prepare_favicon_asset


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
    hero_image_asset = models.ForeignKey(
        "media.MediaAsset",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="hero_site_settings",
    )
    hero_image_alt_en = models.CharField(
        blank=True,
        help_text="English alternative text for the selected hero image.",
        max_length=255,
    )
    hero_image_alt_es = models.CharField(
        blank=True,
        help_text="Optional Spanish alternative text for the selected hero image.",
        max_length=255,
    )
    favicon = models.ImageField(
        blank=True,
        help_text="The small image shown in the browser tab.",
        upload_to="site/favicon/",
    )
    favicon_asset = models.ForeignKey(
        "media.MediaAsset",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="favicon_site_settings",
    )
    homepage_icon_1_asset = models.ForeignKey(
        "media.MediaAsset",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="homepage_icon_1_site_settings",
    )
    homepage_icon_2_asset = models.ForeignKey(
        "media.MediaAsset",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="homepage_icon_2_site_settings",
    )
    homepage_icon_3_asset = models.ForeignKey(
        "media.MediaAsset",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="homepage_icon_3_site_settings",
    )
    homepage_icon_4_asset = models.ForeignKey(
        "media.MediaAsset",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="homepage_icon_4_site_settings",
    )
    homepage_icon_5_asset = models.ForeignKey(
        "media.MediaAsset",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="homepage_icon_5_site_settings",
    )
    homepage_icon_6_asset = models.ForeignKey(
        "media.MediaAsset",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="homepage_icon_6_site_settings",
    )
    homepage_icon_7_asset = models.ForeignKey(
        "media.MediaAsset",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="homepage_icon_7_site_settings",
    )
    homepage_statement_1_en = models.CharField(blank=True, max_length=255)
    homepage_statement_1_es = models.CharField(blank=True, max_length=255)
    homepage_statement_2_en = models.CharField(blank=True, max_length=255)
    homepage_statement_2_es = models.CharField(blank=True, max_length=255)
    homepage_statement_3_en = models.CharField(blank=True, max_length=255)
    homepage_statement_3_es = models.CharField(blank=True, max_length=255)
    homepage_statement_4_en = models.CharField(blank=True, max_length=255)
    homepage_statement_4_es = models.CharField(blank=True, max_length=255)
    homepage_statement_5_en = models.CharField(blank=True, max_length=255)
    homepage_statement_5_es = models.CharField(blank=True, max_length=255)
    homepage_statement_6_en = models.CharField(blank=True, max_length=255)
    homepage_statement_6_es = models.CharField(blank=True, max_length=255)
    homepage_statement_7_en = models.CharField(blank=True, max_length=255)
    homepage_statement_7_es = models.CharField(blank=True, max_length=255)
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
        hero_selected = self.hero_image_asset or self.hero_image
        hero_alt_en = (
            self.hero_image_alt_en
            or (self.hero_image_asset.alt_text_en if self.hero_image_asset else "")
            or self.hero_image_alt
        )
        if hero_selected and not hero_alt_en.strip():
            raise ValidationError(
                {"hero_image_alt_en": _("Add English alternative text for the hero image.")}
            )

    def get_hero_image(self):
        """Return the selected media file, falling back during migration."""
        if self.hero_image_asset and self.hero_image_asset.storage_status != "missing":
            return self.hero_image_asset.file
        return self.hero_image

    def get_favicon(self):
        """Return the selected favicon file, falling back during migration."""
        if self.favicon_asset and self.favicon_asset.storage_status != "missing":
            return self.favicon_asset.file
        return self.favicon

    def get_hero_image_alt(self, language="en"):
        """Return localized hero alternative text with an English fallback."""
        if language == "es":
            return (
                self.hero_image_alt_es
                or (self.hero_image_asset.alt_text_es if self.hero_image_asset else "")
                or self.hero_image_alt_en
                or (self.hero_image_asset.alt_text_en if self.hero_image_asset else "")
                or self.hero_image_alt
            )
        return (
            self.hero_image_alt_en
            or (self.hero_image_asset.alt_text_en if self.hero_image_asset else "")
            or self.hero_image_alt
        )

    def get_homepage_icons(self):
        """Return the seven fixed homepage icon asset references."""
        return tuple(
            getattr(self, f"homepage_icon_{number}_asset")
            for number in range(1, 8)
        )

    def get_homepage_statements(self, language="en"):
        """Return the seven fixed statements with intentional Spanish fallback."""
        use_spanish = (language or "en").split("-")[0] == "es"
        statements = []
        for number, asset in enumerate(self.get_homepage_icons(), start=1):
            english = getattr(self, f"homepage_statement_{number}_en")
            spanish = getattr(self, f"homepage_statement_{number}_es")
            statements.append(
                {
                    "asset": asset,
                    "text": spanish if use_spanish and spanish else english,
                }
            )
        return tuple(statements)

    def homepage_statements_ready(self):
        """Return whether all seven assets and English statements are configured."""
        return all(
            asset
            and asset.storage_status != "missing"
            and asset.file.name
            and getattr(self, f"homepage_statement_{number}_en").strip()
            for number, asset in enumerate(self.get_homepage_icons(), start=1)
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
        if self.favicon_asset:
            self.favicon_asset = prepare_favicon_asset(self.favicon_asset)
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
    photo_asset = models.ForeignKey(
        "media.MediaAsset",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="team_member_photos",
    )
    photo_alt = models.CharField(
        blank=True,
        help_text="Describe the photo for visitors using a screen reader.",
        max_length=255,
    )
    photo_alt_es = models.CharField(
        blank=True,
        help_text="Optional Spanish alternative text for the selected photo.",
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
        photo_selected = self.photo_asset or self.photo
        photo_alt = self.photo_alt or (
            self.photo_asset.alt_text_en if self.photo_asset else ""
        )
        if photo_selected and not photo_alt.strip():
            raise ValidationError({"photo_alt": _("Add alternative text for the photo.")})

    def get_photo(self):
        """Return the selected media file, falling back during migration."""
        if self.photo_asset and self.photo_asset.storage_status != "missing":
            return self.photo_asset.file
        return self.photo

    def get_photo_alt(self, language="en"):
        """Return localized photo alternative text with an English fallback."""
        if language == "es":
            return (
                self.photo_alt_es
                or (self.photo_asset.alt_text_es if self.photo_asset else "")
                or self.photo_alt
            )
        return self.photo_alt or (
            self.photo_asset.alt_text_en if self.photo_asset else ""
        )

    def __str__(self):
        return f"{self.name} - {self.role}"
