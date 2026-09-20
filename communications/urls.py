from django.urls import path

from .views import (
    planting_interest,
    subscribe,
    subscribe_confirmed,
    template_preview,
    unsubscribe,
)

app_name = "communications"

urlpatterns = [
    path("", subscribe, name="subscribe"),
    path("confirmed/", subscribe_confirmed, name="subscribe-confirmed"),
    path("planting-interest/", planting_interest, name="planting-interest"),
    path("unsubscribe/<uuid:token>/", unsubscribe, name="unsubscribe"),
    path(
        "templates/<int:template_id>/preview/",
        template_preview,
        name="template-preview",
    ),
]
