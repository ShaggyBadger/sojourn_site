from django.shortcuts import render

from .models import TeamMember


def home(request):
    """Render the homepage using the current site-wide settings."""
    team_members = TeamMember.objects.filter(is_published=True)
    return render(request, "home.html", {"team_members": team_members})
