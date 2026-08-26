from django.contrib import admin

from .models import AboutPage, AboutSection, SiteSettings, TeamMember


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Homepage hero",
            {
                "fields": ("hero_image", "hero_image_alt"),
                "description": "Upload the image that should appear in the homepage hero section.",
            },
        ),
        (
            "Browser favicon",
            {
                "fields": ("favicon",),
                "description": "Upload the image shown in the browser tab.",
            },
        ),
    )

    def has_add_permission(self, request):
        """Only allow the single site-settings record to exist."""
        return not SiteSettings.objects.exists()


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
            {"fields": ("name", "photo", "photo_alt")},
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
