from django.db.models import Prefetch

from .models import SermonTranslation


def with_spanish_translation(queryset):
    """Prefetch the optional Spanish translation without extra queries per sermon."""
    return queryset.prefetch_related(
        Prefetch(
            "translations",
            queryset=SermonTranslation.objects.filter(
                language=SermonTranslation.Language.SPANISH
            ),
            to_attr="spanish_translations",
        )
    )


def localize_sermon(sermon, language):
    """Expose translated display values while preserving the English source fields."""
    translation = None
    if language == SermonTranslation.Language.SPANISH:
        translation = next(iter(getattr(sermon, "spanish_translations", ())), None)

    for field in ("title", "summary", "thesis", "transcript"):
        translated_value = getattr(translation, field, "") if translation else ""
        setattr(sermon, f"display_{field}", translated_value or getattr(sermon, field))
    return sermon


def has_complete_spanish_translation(sermon):
    """Return whether all substantive sermon content has a Spanish translation."""
    translations = getattr(sermon, "spanish_translations", None)
    if translations is None:
        translations = sermon.translations.filter(
            language="es"
        )
    translation = next(iter(translations), None)
    if translation is None:
        return False

    required_fields = ["title", "summary", "thesis"]
    if sermon.transcript:
        required_fields.append("transcript")
    return all(getattr(translation, field) for field in required_fields)
