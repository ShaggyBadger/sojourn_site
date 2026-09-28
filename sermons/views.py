from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import translate_url
from django.utils.translation import get_language
from django.views.generic import DetailView, ListView

from core.seo import build_sermon_structured_data

from .localization import (
    has_complete_spanish_translation,
    localize_sermon,
    with_spanish_translation,
)
from .models import Sermon, SermonCollection, SermonTag


def set_taxonomy_language_metadata(context, request):
    """Keep untranslated Spanish taxonomy pages out of search indexes."""
    context["alternate_language_urls"] = [
        alternate
        for alternate in context.get("alternate_language_urls", ())
        if alternate["language"] == settings.LANGUAGE_CODE
    ]
    if get_language() != "es":
        return

    english_path = translate_url(request.path, settings.LANGUAGE_CODE)
    site_url = settings.PUBLIC_SITE_URL.rstrip("/")
    context["canonical_url"] = f"{site_url}{english_path}"
    context["robots_noindex"] = True


class PublishedSermonQuerySetMixin:
    def get_queryset(self):
        queryset = (
            Sermon.objects.filter(is_published=True)
            .select_related("collection")
            .prefetch_related("tags")
        )
        return with_spanish_translation(queryset)


class SermonListView(PublishedSermonQuerySetMixin, ListView):
    template_name = "sermons/sermon_list.html"
    context_object_name = "sermons"
    paginate_by = 10

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
        for sermon in context["sermons"]:
            localize_sermon(sermon, get_language())
        return context


class SermonDetailView(PublishedSermonQuerySetMixin, DetailView):
    template_name = "sermons/sermon_detail.html"
    context_object_name = "sermon"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = get_language()
        localize_sermon(self.object, language)
        spanish_translation_complete = has_complete_spanish_translation(self.object)
        context["spanish_translation_complete"] = spanish_translation_complete
        if not spanish_translation_complete:
            context["alternate_language_urls"] = [
                alternate
                for alternate in context.get("alternate_language_urls", ())
                if alternate["language"] == settings.LANGUAGE_CODE
            ]
        if language == "es" and not spanish_translation_complete:
            english_path = translate_url(self.request.path, settings.LANGUAGE_CODE)
            site_url = settings.PUBLIC_SITE_URL.rstrip("/")
            context["canonical_url"] = f"{site_url}{english_path}"
        context["sermon_structured_data"] = None
        if language != "es" or spanish_translation_complete:
            context["sermon_structured_data"] = build_sermon_structured_data(
                self.object, settings.PUBLIC_SITE_URL, language
            )
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
        context["sermons"] = with_spanish_translation(context["sermons"])
        context["sermons"] = [
            localize_sermon(sermon, get_language()) for sermon in context["sermons"]
        ]
        context["sermon_count"] = len(context["sermons"])
        set_taxonomy_language_metadata(context, self.request)
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
        context["sermons"] = with_spanish_translation(context["sermons"])
        context["sermons"] = [
            localize_sermon(sermon, get_language()) for sermon in context["sermons"]
        ]
        context["sermon_count"] = len(context["sermons"])
        set_taxonomy_language_metadata(context, self.request)
        return context
