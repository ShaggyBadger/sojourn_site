from django.urls import path

from .views import (
    SermonCollectionDetailView,
    SermonDetailView,
    SermonListView,
    SermonTagDetailView,
)

app_name = "sermons"

urlpatterns = [
    path("", SermonListView.as_view(), name="list"),
    path("collection/<slug:slug>/", SermonCollectionDetailView.as_view(), name="collection_detail"),
    path("tag/<slug:slug>/", SermonTagDetailView.as_view(), name="tag_detail"),
    path("<slug:slug>/", SermonDetailView.as_view(), name="detail"),
]
