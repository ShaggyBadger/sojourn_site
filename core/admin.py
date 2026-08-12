from django.contrib import admin

from .models import SiteSettings, TeamMember


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
