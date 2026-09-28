from django.conf import settings
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.views import (
    about,
    belief_detail,
    beliefs,
    confession,
    giving,
    home,
    how_we_are_led,
    new_here,
    partner_with_us,
    robots_txt,
)
from core.sitemaps import SermonSitemap, StaticViewSitemap
from sermons.api import (
    collection_list,
    sermon_upload,
    translation_job_claim,
    translation_job_submit,
)

sitemaps = {
    "static": StaticViewSitemap,
    "sermons": SermonSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("api/v1/sermons/", sermon_upload, name="sermon_upload"),
    path("api/v1/sermons/collections/", collection_list, name="sermon_collections"),
    path("api/v1/translation-jobs/claim/", translation_job_claim, name="translation_job_claim"),
    path(
        "api/v1/translation-jobs/<int:job_id>/submit/",
        translation_job_submit,
        name="translation_job_submit",
    ),
]

urlpatterns += i18n_patterns(
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("how-we-are-led/", how_we_are_led, name="how_we_are_led"),
    path("partner-with-us/", partner_with_us, name="partner_with_us"),
    path("what-we-believe/", beliefs, name="beliefs"),
    path("new-hampshire-confession-of-faith/", confession, name="confession"),
    path("new-here/", new_here, name="new_here"),
    path("giving/", giving, name="giving"),
    path("sermons/", include("sermons.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "subscribe/",
        include(("communications.urls", "communications"), namespace="communications"),
    ),
    path("<slug:slug>/", belief_detail, name="belief_detail"),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
