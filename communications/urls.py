from django.urls import path

from .views import subscribe, template_preview, unsubscribe

app_name = "communications"

urlpatterns = [
    path("", subscribe, name="subscribe"),
    path("unsubscribe/<uuid:token>/", unsubscribe, name="unsubscribe"),
    path(
        "templates/<int:template_id>/preview/",
        template_preview,
        name="template-preview",
    ),
]
