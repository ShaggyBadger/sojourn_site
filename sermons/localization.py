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
