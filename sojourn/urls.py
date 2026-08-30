from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.views import about, giving, home, new_here, robots_txt
from core.sitemaps import SermonSitemap, StaticViewSitemap
from sermons.api import sermon_upload

sitemaps = {
    "static": StaticViewSitemap,
    "sermons": SermonSitemap,
}

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("new-here/", new_here, name="new_here"),
    path("giving/", giving, name="giving"),
    path("sermons/", include("sermons.urls")),
    path("admin/", admin.site.urls),
    path(
        "subscribe/",
        include(("communications.urls", "communications"), namespace="communications"),
    ),
    path("i18n/", include("django.conf.urls.i18n")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("api/v1/sermons/", sermon_upload, name="sermon_upload"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
