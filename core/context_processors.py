from django.conf import settings
from django.utils.translation import get_language

from .models import SiteSettings
from .seo import build_site_structured_data


def site_settings(request):
    """Make site-wide branding available to every template."""
    site_settings = SiteSettings.objects.first()
    return {
        "site_settings": site_settings,
        "site_hero_image": site_settings.get_hero_image() if site_settings else None,
        "site_hero_image_alt": (
            site_settings.get_hero_image_alt(get_language()) if site_settings else ""
        ),
        "site_favicon": site_settings.get_favicon() if site_settings else None,
        "active_theme": (
            site_settings.get_effective_theme()
            if site_settings
            else SiteSettings.DEFAULT_THEME
        ),
        "public_site_url": settings.PUBLIC_SITE_URL.rstrip("/"),
        "site_structured_data": build_site_structured_data(request, site_settings),
    }
