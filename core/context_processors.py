from django.conf import settings
from django.urls import translate_url
from django.utils.translation import get_language

from .models import SiteSettings
from .seo import build_site_structured_data


def site_settings(request):
    """Make site-wide branding available to every template."""
    site_settings = SiteSettings.objects.first()
    site_url = settings.PUBLIC_SITE_URL.rstrip("/")
    alternate_language_urls = []
    for language_code, _ in settings.LANGUAGES:
        translated_path = translate_url(request.path, language_code)
        if translated_path:
            alternate_language_urls.append(
                {
                    "language": language_code,
                    "url": f"{site_url}{translated_path}",
                }
            )
    if len({alternate["url"] for alternate in alternate_language_urls}) < 2:
        alternate_language_urls = []
    resolver_match = getattr(request, "resolver_match", None)
    if resolver_match and resolver_match.namespace == "communications":
        alternate_language_urls = []

    return {
        "site_settings": site_settings,
        "site_hero_image": site_settings.get_hero_image() if site_settings else None,
        "site_hero_image_alt": (
            site_settings.get_hero_image_alt(get_language()) if site_settings else ""
        ),
        "site_favicon": site_settings.get_favicon() if site_settings else None,
        "social_links": (
            site_settings.social_links.filter(is_published=True) if site_settings else ()
        ),
        "active_theme": (
            site_settings.get_effective_theme()
            if site_settings
            else SiteSettings.DEFAULT_THEME
        ),
        "public_site_url": site_url,
        "canonical_url": f"{site_url}{request.path}",
        "alternate_language_urls": alternate_language_urls,
        "site_structured_data": build_site_structured_data(request, site_settings),
    }
