from django import forms
from django.urls import reverse
from django.utils.html import format_html


class MediaAssetPickerWidget(forms.Select):
    """Add a separate-window media browser beside an asset select field."""

    class Media:
        js = ("media/js/media_asset_picker.js",)

    def render(self, name, value, attrs=None, renderer=None):
        select_html = super().render(name, value, attrs, renderer)
        field_id = (attrs or {}).get("id", f"id_{name}")
        return format_html(
            '<div class="media-asset-picker-field">{} '
            '<button type="button" class="button media-asset-picker-button" '
            'data-picker-url="{}" data-field-id="{}">Browse media library</button>'
            '</div>',
            select_html,
            reverse("admin:media_mediaasset_picker"),
            field_id,
        )
