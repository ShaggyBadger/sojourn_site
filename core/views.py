from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import get_language

from .models import SiteSettings, TeamMember
from .beliefs import BELIEF_SUMMARIES, get_belief_page
from .confession import (
    CONFESSION_SOURCE_URL,
    CONFESSION_TITLE,
    get_confession_articles,
)
from .polity import get_polity_page
from .partner import get_partner_page
from .selectors import get_localized_about_content
from sermons.models import Sermon
from sermons.localization import localize_sermon, with_spanish_translation


GIVING_URL = "https://www.zeffy.com/en-US/donation-form/tithegive-to-sojourn-church"


def home(request):
    """Render the homepage using the current site-wide settings."""
    site_settings = SiteSettings.objects.first()
    homepage_icons = site_settings.get_homepage_icons() if site_settings else ()
    homepage_statements = (
        site_settings.get_homepage_statements(get_language()) if site_settings else ()
    )
    homepage_statements_ready = (
        site_settings.homepage_statements_ready() if site_settings else False
    )
    latest_sermon = with_spanish_translation(
        Sermon.objects.filter(
            is_published=True,
            sermon_date__lte=timezone.localdate(),
        )
        .order_by("-sermon_date", "-created_at")
    ).first()
    if latest_sermon:
        localize_sermon(latest_sermon, get_language())
    return render(
        request,
        "home.html",
        {
            "homepage_statements": homepage_statements,
            "homepage_statements_ready": homepage_statements_ready,
            "latest_sermon": latest_sermon,
        },
    )


def about(request):
    """Render the published, database-driven About page."""
    about_content = get_localized_about_content()
    if about_content is None:
        raise Http404("The About page is not published.")

    has_leadership_section = any(
        section.key == "leadership" for section in about_content.sections
    )
    team_members = (
        TeamMember.objects.filter(is_published=True) if has_leadership_section else ()
    )
    return render(
        request,
        "about.html",
        {"about_content": about_content, "team_members": team_members},
    )


def confession(request):
    """Render the historical 1853 New Hampshire Confession of Faith."""
    return render(
        request,
        "confession.html",
        {
            "confession_articles": get_confession_articles(get_language()),
            "confession_source_url": CONFESSION_SOURCE_URL,
            "confession_title": CONFESSION_TITLE,
        },
    )


def beliefs(request):
    """Render the beliefs hub with links to each dedicated statement page."""
    language = get_language()
    is_spanish = (language or "en").split("-")[0] == "es"
    summaries = []
    for summary in BELIEF_SUMMARIES:
        summaries.append(
            {
                "slug": summary["slug"],
                "title": summary["title_es"] if is_spanish else summary["title"],
                "summary": summary["summary_es"] if is_spanish else summary["summary"],
            }
        )
    return render(request, "beliefs.html", {"belief_summaries": summaries})


def belief_detail(request, slug):
    """Render one of the church's dedicated belief and creed pages."""
    if slug not in {summary["slug"] for summary in BELIEF_SUMMARIES}:
        raise Http404("The requested statement of faith was not found.")
    page = get_belief_page(slug, get_language())
    return render(request, "belief_detail.html", {"belief_page": page})


def how_we_are_led(request):
    """Render the bilingual explanation of Sojourn's church leadership."""
    return render(request, "how_we_are_led.html", {"polity_page": get_polity_page(get_language())})


def partner_with_us(request):
    """Render the bilingual ways visitors can partner with Sojourn."""
    return render(request, "partner_with_us.html", {"partner_page": get_partner_page(get_language())})


def new_here(request):
    """Render practical visitor information for a first visit."""
    return render(request, "new_here.html")


def giving(request):
    """Render information about giving and link to the church's Zeffy form."""
    return render(request, "giving.html", {"giving_url": GIVING_URL})


def robots_txt(request):
    """Tell crawlers what to index and where to find the sitemap."""
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    return HttpResponse(
        f"# Welcome, curious crawler.\n"
        f"# Sojourn Church is a bilingual church community in Mount Airy, NC.\n"
        f"# Thanks for helping people find our church and sermons.\n"
        f"\n"
        f"User-agent: *\n"
        f"Allow: /\n"
        f"Disallow: /admin/\n"
        f"Disallow: /subscribe/\n"
        f"Sitemap: {sitemap_url}\n",
        content_type="text/plain",
    )
