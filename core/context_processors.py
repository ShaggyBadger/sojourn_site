from django.conf import settings

from .models import SiteSettings
from .seo import build_site_structured_data


def site_settings(request):
    """Make site-wide branding available to every template."""
    site_settings = SiteSettings.objects.first()
    return {
        "site_settings": site_settings,
        "public_site_url": settings.PUBLIC_SITE_URL.rstrip("/"),
        "site_structured_data": build_site_structured_data(request, site_settings),
    }
