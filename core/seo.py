import json

from django.conf import settings
from django.utils.safestring import mark_safe


def serialize_json_ld(value):
    """Serialize JSON-LD safely for an application/ld+json script element."""
    serialized = json.dumps(value, ensure_ascii=True, separators=(",", ":"))
    serialized = serialized.replace("<", "\\u003c")
    serialized = serialized.replace(">", "\\u003e")
    serialized = serialized.replace("&", "\\u0026")
    return mark_safe(serialized)


def build_site_structured_data(request, site_settings):
    """Build the shared church, website, and current-page JSON-LD graph."""
    site_url = settings.PUBLIC_SITE_URL.rstrip("/")
    church_id = f"{site_url}/#church"
    website_id = f"{site_url}/#website"
    page_url = f"{site_url}{request.path}"

    church = {
        "@type": "Church",
        "@id": church_id,
        "name": settings.SEO_CHURCH_NAME,
        "url": site_url,
        "description": settings.SEO_CHURCH_DESCRIPTION,
        "areaServed": settings.SEO_CHURCH_AREA_SERVED,
    }
    if site_settings and site_settings.get_hero_image():
        church["image"] = site_settings.get_hero_image().url

    graph = [
        church,
        {
            "@type": "WebSite",
            "@id": website_id,
            "url": site_url,
            "name": settings.SEO_CHURCH_NAME,
            "publisher": {"@id": church_id},
        },
        {
            "@type": "WebPage",
            "@id": f"{page_url}#webpage",
            "url": page_url,
            "isPartOf": {"@id": website_id},
            "about": {"@id": church_id},
            "inLanguage": getattr(request, "LANGUAGE_CODE", "en"),
        },
    ]
    return serialize_json_ld({"@context": "https://schema.org", "@graph": graph})


def build_sermon_structured_data(sermon, site_url):
    """Build JSON-LD for a published sermon without duplicating the Church entity."""
    site_url = site_url.rstrip("/")
    sermon_url = f"{site_url}/sermons/{sermon.slug}/"
    return serialize_json_ld(
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "@id": f"{sermon_url}#article",
            "url": sermon_url,
            "headline": sermon.title,
            "description": sermon.summary,
            "datePublished": sermon.sermon_date.isoformat(),
            "author": {"@type": "Person", "name": sermon.speaker},
            "publisher": {"@id": f"{site_url}/#church"},
            "mainEntityOfPage": {"@id": f"{sermon_url}#webpage"},
        }
    )
