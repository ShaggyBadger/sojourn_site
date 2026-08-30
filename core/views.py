from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from .models import TeamMember
from .selectors import get_localized_about_content
from sermons.models import Sermon


GIVING_URL = "https://www.zeffy.com/en-US/donation-form/tithegive-to-sojourn-church"


def home(request):
    """Render the homepage using the current site-wide settings."""
    team_members = TeamMember.objects.filter(is_published=True)
    latest_sermon = (
        Sermon.objects.filter(
            is_published=True,
            sermon_date__lte=timezone.localdate(),
        )
        .order_by("-sermon_date", "-created_at")
        .first()
    )
    return render(
        request,
        "home.html",
        {
            "team_members": team_members,
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
