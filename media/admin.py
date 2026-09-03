from django.contrib import admin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import format_html

from .models import MediaAsset, MediaCleanupIssue, MediaTag


@admin.register(MediaTag)
class MediaTagAdmin(admin.ModelAdmin):
    list_display = ("name", "normalized_name")
    search_fields = ("name", "normalized_name")
    readonly_fields = ("normalized_name",)


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = (
        "preview",
        "name",
        "media_type",
        "file_size_display",
        "dimensions",
        "storage_status",
        "created_at",
    )
    list_filter = ("media_type", "storage_status", "tags", "created_at")
    search_fields = ("name", "description", "original_filename", "tags__name")
    filter_horizontal = ("tags",)
    readonly_fields = (
        "preview",
        "original_filename",
        "mime_type",
        "file_size",
        "width",
        "height",
        "sha256",
        "storage_status",
        "uploaded_by",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Asset",
            {
                "fields": ("file", "preview", "name", "description", "tags"),
                "description": "Media assets are publicly reachable when uploaded.",
            },
        ),
        (
            "Alternative text",
            {"fields": ("alt_text_en", "alt_text_es")},
        ),
        (
            "File information",
            {
                "fields": (
                    "original_filename",
                    "mime_type",
                    "file_size",
                    "width",
                    "height",
                    "sha256",
                    "storage_status",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "System",
            {"fields": ("uploaded_by", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    @admin.display(description="Preview")
    def preview(self, obj):
        if not obj or not obj.file:
            return "No image"
        return format_html(
            '<img src="{}" alt="" style="max-height: 80px; max-width: 140px;">',
            obj.file.url,
        )

    @admin.display(description="Size")
    def file_size_display(self, obj):
        return f"{obj.file_size / (1024 * 1024):.2f} MiB"

    @admin.display(description="Dimensions")
    def dimensions(self, obj):
        if not obj.width or not obj.height:
            return "-"
        return f"{obj.width} x {obj.height}"

    def save_model(self, request, obj, form, change):
        if not change and not obj.uploaded_by_id:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "picker/",
                self.admin_site.admin_view(self.picker_view),
                name="media_mediaasset_picker",
            ),
        ]
        return custom_urls + urls

    def picker_view(self, request):
        """Render the searchable image picker used by assignment fields."""
        if not self.has_view_permission(request):
            return HttpResponseForbidden()

        query = request.GET.get("q", "").strip()
        selected_tag = request.GET.get("tag", "").strip()
        assets = MediaAsset.objects.filter(
            storage_status=MediaAsset.StorageStatus.PRESENT,
        ).prefetch_related("tags")
        if query:
            assets = assets.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(original_filename__icontains=query)
            )
        if selected_tag.isdigit():
            assets = assets.filter(tags__pk=int(selected_tag))

        page_obj = Paginator(assets.order_by("name"), 30).get_page(
            request.GET.get("page", 1)
        )
        context = {
            **self.admin_site.each_context(request),
            "assets": page_obj.object_list,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "field_id": request.GET.get("field_id", ""),
            "query": query,
            "selected_tag": selected_tag,
            "tags": MediaTag.objects.order_by("name"),
            "title": "Choose a media asset",
        }
        return TemplateResponse(request, "admin/media/mediaasset/picker.html", context)

@admin.register(MediaCleanupIssue)
class MediaCleanupIssueAdmin(admin.ModelAdmin):
    list_display = ("storage_key", "reason", "created_at", "resolved_at")
    list_filter = ("resolved_at", "created_at")
    search_fields = ("storage_key", "reason", "last_error")
    readonly_fields = ("storage_key", "reason", "last_error", "created_at", "resolved_at")
