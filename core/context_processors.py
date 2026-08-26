from .models import SiteSettings


def site_settings(request):
    """Make site-wide branding available to every template."""
    return {"site_settings": SiteSettings.objects.first()}
