from django.shortcuts import render


def home(request):
    """Render the homepage using the current site-wide settings."""
    return render(request, "home.html")
