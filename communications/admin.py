from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import EmailRecipient, EmailTemplate, RecipientGroup


@admin.register(EmailRecipient)
class EmailRecipientAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "status",
        "source",
        "updated_at",
    )
    list_filter = ("status", "source")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("last_name", "first_name", "email")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Contact",
            {"fields": ("email", "first_name", "last_name")},
        ),
        (
            "Delivery status",
            {"fields": ("status", "source", "consent_at", "unsubscribed_at")},
        ),
        (
            "Record history",
            {"fields": ("created_at", "updated_at")},
        ),
    )


@admin.register(RecipientGroup)
class RecipientGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "member_count", "updated_at")
    search_fields = ("name", "description")
    ordering = ("name",)
    filter_horizontal = ("members",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Group",
            {"fields": ("name", "description", "members")},
        ),
        (
            "Record history",
            {"fields": ("created_at", "updated_at")},
        ),
    )

    @admin.display(description="Members")
    def member_count(self, obj):
        return obj.members.count()


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "layout",
        "language",
        "is_active",
        "updated_at",
        "preview_link",
    )
    list_filter = ("layout", "language", "is_active")
    search_fields = ("name", "description", "subject_template")
    ordering = ("name",)
    readonly_fields = ("created_by", "created_at", "updated_at")
    fieldsets = (
        (
            "Template",
            {
                "fields": (
                    "name",
                    "description",
                    "layout",
                    "language",
                    "is_active",
                )
            },
        ),
        (
            "Weekly meeting content",
            {
                "fields": (
                    "subject_template",
                    "greeting",
                    "standard_copy",
                    "body_html",
                    "closing",
                )
            },
        ),
        (
            "Record history",
            {"fields": ("created_by", "created_at", "updated_at")},
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description="Preview")
    def preview_link(self, obj):
        url = reverse("communications:template-preview", args=(obj.pk,))
        return format_html('<a href="{}">Open preview</a>', url)
