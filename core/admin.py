from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from media.models import MediaAsset
from media.widgets import MediaAssetPickerWidget

from .models import AboutPage, AboutSection, SiteSettings, TeamMember


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ("homepage_icon_status",)
    fieldsets = (
        (
            "Homepage hero",
            {
                "fields": ("hero_image_asset", "hero_image_alt_en", "hero_image_alt_es"),
                "description": "Select the image that should appear in the homepage hero section.",
            },
        ),
        (
            "Browser favicon",
            {
                "fields": ("favicon_asset",),
                "description": _(
                    "Select an image for the browser tab. Non-square images are "
                    "automatically centered and converted to a 512 x 512 PNG."
                ),
            },
        ),
        (
            "Appearance",
            {
                "fields": ("theme",),
                "description": "This choice changes the presentation of the entire public website.",
            },
        ),
        (
            "Homepage icons",
            {
                "fields": (
                    "homepage_icon_1_asset",
                    "homepage_icon_2_asset",
                    "homepage_icon_3_asset",
                    "homepage_icon_4_asset",
                    "homepage_icon_5_asset",
                    "homepage_icon_6_asset",
                    "homepage_icon_7_asset",
                    "homepage_icon_status",
                ),
                "description": "Assign all seven icons before the homepage section is shown.",
            },
        ),
        (
            "Homepage statements",
            {
                "fields": (
                    ("homepage_statement_1_en", "homepage_statement_1_es"),
                    ("homepage_statement_2_en", "homepage_statement_2_es"),
                    ("homepage_statement_3_en", "homepage_statement_3_es"),
                    ("homepage_statement_4_en", "homepage_statement_4_es"),
                    ("homepage_statement_5_en", "homepage_statement_5_es"),
                    ("homepage_statement_6_en", "homepage_statement_6_es"),
                    ("homepage_statement_7_en", "homepage_statement_7_es"),
                ),
                "description": "Enter English statements here. Spanish translations are pre-filled and can be edited if needed.",
            },
        ),
    )

    def has_add_permission(self, request):
        """Only allow the single site-settings record to exist."""
        return not SiteSettings.objects.exists()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.remote_field.model is MediaAsset:
            kwargs["widget"] = MediaAssetPickerWidget()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(description="Homepage icon status")
    def homepage_icon_status(self, obj):
        if not obj:
            return "Save settings to check"
        assigned = sum(asset is not None for asset in obj.get_homepage_icons())
        if assigned == 7:
            return "Complete"
        return f"{assigned} of 7 assigned"


class AboutSectionInline(admin.StackedInline):
    model = AboutSection
    extra = 0
    ordering = ("display_order", "key")
    fields = (
        "key",
        "title_en",
        "title_es",
        "body_en",
        "body_es",
        "display_order",
        "is_visible",
        "translation_status",
    )
    readonly_fields = ("translation_status",)

    @admin.display(description="Spanish status")
    def translation_status(self, obj):
        if not obj:
            return "Save section to check"
        if obj.key == "leadership":
            complete = obj.title_es.strip()
        else:
            complete = obj.title_es.strip() and obj.body_es.strip()
        if complete:
            return "Complete"
        return "Spanish translation needed"


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    inlines = (AboutSectionInline,)
    fieldsets = (
        (
            "English page content",
            {"fields": ("title_en", "meta_description_en")},
        ),
        (
            "Spanish page content",
            {"fields": ("title_es", "meta_description_es")},
        ),
        (
            "Publishing",
            {"fields": ("is_published", "updated_at")},
        ),
    )
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        """Only allow the single About page record to exist."""
        return not AboutPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Keep the About page available for administrators."""
        return False


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", "is_published")
    list_editable = ("order", "is_published")
    list_display_links = ("name",)
    ordering = ("order", "name")
    fieldsets = (
        (
            "Identity",
            {"fields": ("name", "photo_asset", "photo_alt", "photo_alt_es")},
        ),
        (
            "English content",
            {"fields": ("role", "bio")},
        ),
        (
            "Spanish content",
            {"fields": ("role_es", "bio_es")},
        ),
        (
            "Publishing",
            {"fields": ("order", "is_published")},
        ),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.remote_field.model is MediaAsset:
            kwargs["widget"] = MediaAssetPickerWidget()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
