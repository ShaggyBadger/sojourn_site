from django.contrib import admin

from .models import Sermon, SermonCollection, SermonTag


@admin.register(SermonCollection)
class SermonCollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(SermonTag)
class SermonTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ("title", "sermon_date", "speaker", "collection", "is_published")
    list_filter = ("is_published", "collection", "sermon_date", "tags")
    list_editable = ("is_published",)
    list_display_links = ("title",)
    date_hierarchy = "sermon_date"
    ordering = ("-sermon_date", "-created_at")
    search_fields = (
        "title",
        "speaker",
        "summary",
        "thesis",
        "main_scripture",
        "transcript",
        "tags__name",
    )
    filter_horizontal = ("tags",)
    readonly_fields = ("slug", "created_at", "updated_at")
    fieldsets = (
        (
            "Sermon content",
            {
                "fields": (
                    "title",
                    "speaker",
                    "sermon_date",
                    "summary",
                    "thesis",
                    "main_scripture",
                    "transcript",
                )
            },
        ),
        (
            "Audio",
            {
                "fields": ("media_file",),
                "description": "Upload an MP3 file up to 100 MB.",
            },
        ),
        (
            "Organization",
            {"fields": ("collection", "tags")},
        ),
        (
            "Publishing",
            {"fields": ("is_published", "published_at")},
        ),
        (
            "System",
            {"fields": ("slug", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    autocomplete_fields = ("collection",)
