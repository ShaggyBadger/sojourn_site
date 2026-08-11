from django.contrib import admin

from .models import SiteSettings


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
