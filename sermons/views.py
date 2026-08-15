from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .models import Sermon, SermonCollection, SermonTag


class PublishedSermonQuerySetMixin:
    def get_queryset(self):
        return (
            Sermon.objects.filter(is_published=True)
            .select_related("collection")
            .prefetch_related("tags")
        )


class SermonListView(PublishedSermonQuerySetMixin, ListView):
    template_name = "sermons/sermon_list.html"
    context_object_name = "sermons"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        collection_slug = self.request.GET.get("collection", "").strip()
        tag_slug = self.request.GET.get("tag", "").strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(speaker__icontains=query)
                | Q(summary__icontains=query)
                | Q(thesis__icontains=query)
                | Q(main_scripture__icontains=query)
                | Q(transcript__icontains=query)
                | Q(collection__name__icontains=query)
                | Q(tags__name__icontains=query)
            )
        if collection_slug:
            queryset = queryset.filter(
                collection__slug=collection_slug,
                collection__is_published=True,
            )
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        selected_collection = self.request.GET.get("collection", "").strip()
        selected_tag = self.request.GET.get("tag", "").strip()
        context["query"] = query
        context["selected_collection"] = selected_collection
        context["selected_tag"] = selected_tag
        context["has_filters"] = bool(query or selected_collection or selected_tag)
        context["result_count"] = context["paginator"].count
        context["collections"] = SermonCollection.objects.filter(
            is_published=True,
            sermons__is_published=True,
        ).distinct()
        context["tags"] = SermonTag.objects.filter(
            sermons__is_published=True
        ).distinct()
        context["selected_collection_name"] = (
            SermonCollection.objects.filter(slug=selected_collection)
            .values_list("name", flat=True)
            .first()
            if selected_collection
            else ""
        )
        context["selected_tag_name"] = (
            SermonTag.objects.filter(slug=selected_tag)
            .values_list("name", flat=True)
            .first()
            if selected_tag
            else ""
        )
        return context


class SermonDetailView(PublishedSermonQuerySetMixin, DetailView):
    template_name = "sermons/sermon_detail.html"
    context_object_name = "sermon"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_sermons"] = Sermon.objects.none()
        if self.object.collection:
            context["related_sermons"] = (
                Sermon.objects.filter(
                    collection=self.object.collection,
                    is_published=True,
                )
                .exclude(pk=self.object.pk)
                .order_by("-sermon_date", "-created_at")
            )
        return context


class SermonCollectionDetailView(PublishedSermonQuerySetMixin, DetailView):
    model = SermonCollection
    template_name = "sermons/collection_detail.html"
    context_object_name = "collection"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return SermonCollection.objects.filter(
            is_published=True,
            sermons__is_published=True,
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sermons"] = (
            Sermon.objects.filter(collection=self.object, is_published=True)
            .select_related("collection")
            .prefetch_related("tags")
        )
        context["sermon_count"] = context["sermons"].count()
        return context


class SermonTagDetailView(PublishedSermonQuerySetMixin, DetailView):
    model = SermonTag
    template_name = "sermons/tag_detail.html"
    context_object_name = "tag"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return SermonTag.objects.filter(sermons__is_published=True).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sermons"] = (
            Sermon.objects.filter(tags=self.object, is_published=True)
            .select_related("collection")
            .prefetch_related("tags")
        )
        context["sermon_count"] = context["sermons"].count()
        return context
