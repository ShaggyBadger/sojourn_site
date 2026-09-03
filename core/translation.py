from dataclasses import dataclass

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import models


@dataclass(frozen=True)
class TranslationCandidate:
    """An English model field with a conventional, empty Spanish counterpart."""

    content_type: ContentType
    object_id: int
    source_field: str
    target_field: str
    source_text: str


def iter_translation_candidates():
    """Discover missing Spanish fields using the project's ``_en``/``_es`` convention."""
    for model in apps.get_models():
        if model._meta.abstract or not model._meta.managed:
            continue
        fields = {field.name: field for field in model._meta.get_fields()}
        text_fields = {
            field.name: field
            for field in model._meta.fields
            if isinstance(field, (models.CharField, models.TextField))
            and field.editable
        }
        for source_name, source_field in text_fields.items():
            if not source_name.endswith("_en"):
                continue
            target_name = f"{source_name[:-3]}_es"
            if target_name not in fields or target_name not in text_fields:
                continue
            content_type = ContentType.objects.get_for_model(model)
            for obj in model.objects.order_by("pk"):
                source_text = (getattr(obj, source_name, "") or "").strip()
                target_text = (getattr(obj, target_name, "") or "").strip()
                if source_text and not target_text:
                    yield TranslationCandidate(
                        content_type=content_type,
                        object_id=obj.pk,
                        source_field=source_field.name,
                        target_field=target_name,
                        source_text=source_text,
                    )
