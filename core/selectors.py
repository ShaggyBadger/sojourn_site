from dataclasses import dataclass

from django.utils.translation import get_language

from .models import AboutPage, AboutSection


@dataclass(frozen=True)
class LocalizedAboutSection:
    """A section with content selected for the active site language."""

    key: str
    title: str
    body: str
    display_order: int


@dataclass(frozen=True)
class LocalizedAboutContent:
    """Published About content plus non-public translation fallback status."""

    title: str
    meta_description: str
    sections: tuple[LocalizedAboutSection, ...]
    fallback_keys: tuple[str, ...]


def get_localized_about_content(language=None):
    """Return published About content localized for ``language``.

    Spanish content falls back to English when an editor has not supplied a
    translation. The fallback keys are returned for administrative tracking but
    are not intended for public display.
    """
    page = AboutPage.objects.filter(pk=1, is_published=True).first()
    if page is None:
        return None

    language = (language or get_language() or "en").split("-")[0]
    use_spanish = language == "es"
    fallback_keys = []

    title = page.title_es if use_spanish else page.title_en
    if use_spanish and not title.strip():
        title = page.title_en
        fallback_keys.append("page:title")

    meta_description = (
        page.meta_description_es if use_spanish else page.meta_description_en
    )
    if use_spanish and not meta_description.strip():
        meta_description = page.meta_description_en
        fallback_keys.append("page:meta_description")

    localized_sections = []
    sections = page.sections.filter(is_visible=True).order_by(
        "display_order", "key"
    )
    for section in sections:
        section_title = section.title_es if use_spanish else section.title_en
        section_body = section.body_es if use_spanish else section.body_en
        if use_spanish and not section_title.strip():
            section_title = section.title_en
            fallback_keys.append(f"section:{section.key}:title")
        if use_spanish and not section_body.strip() and section.body_en.strip():
            section_body = section.body_en
            fallback_keys.append(f"section:{section.key}:body")
        localized_sections.append(
            LocalizedAboutSection(
                key=section.key,
                title=section_title,
                body=section_body,
                display_order=section.display_order,
            )
        )

    return LocalizedAboutContent(
        title=title,
        meta_description=meta_description,
        sections=tuple(localized_sections),
        fallback_keys=tuple(fallback_keys),
    )
