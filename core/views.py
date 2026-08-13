from django.http import Http404
from django.shortcuts import render

from .models import TeamMember
from .selectors import get_localized_about_content


def home(request):
    """Render the homepage using the current site-wide settings."""
    team_members = TeamMember.objects.filter(is_published=True)
    return render(request, "home.html", {"team_members": team_members})


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
