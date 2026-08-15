import os
import logging
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


MAX_AUDIO_FILE_SIZE = 100 * 1024 * 1024
logger = logging.getLogger(__name__)


def sermon_audio_upload_path(instance, filename):
    """Keep sermon audio in a recognizable, non-colliding storage prefix."""
    extension = os.path.splitext(filename)[1].lower() or ".mp3"
    return f"sermons/audio/{uuid.uuid4().hex}{extension}"


def validate_mp3(uploaded_file):
    """Enforce the v1 upload policy for browser-compatible sermon audio."""
    if uploaded_file.size > MAX_AUDIO_FILE_SIZE:
        raise ValidationError(_("MP3 files must be 100 MB or smaller."))

    extension = os.path.splitext(uploaded_file.name)[1].lower()
    if extension != ".mp3":
        raise ValidationError(_("Upload an MP3 audio file."))

    content_type = getattr(uploaded_file, "content_type", None)
    if content_type is None:
        # FieldFile values loaded from storage do not retain upload metadata.
        stored_file = getattr(uploaded_file, "_file", None)
        content_type = getattr(stored_file, "content_type", None)
    if content_type is not None and content_type not in {"audio/mpeg", "audio/mp3"}:
        raise ValidationError(_("The uploaded file must be identified as MP3 audio."))


class SermonCollection(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "sermon collection"
        verbose_name_plural = "sermon collections"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SermonTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "sermon tag"
        verbose_name_plural = "sermon tags"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Sermon(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    speaker = models.CharField(max_length=150)
    sermon_date = models.DateField()
    summary = models.TextField()
    thesis = models.TextField()
    main_scripture = models.CharField(max_length=150)
    transcript = models.TextField(blank=True)
    collection = models.ForeignKey(
        SermonCollection,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="sermons",
    )
    tags = models.ManyToManyField(SermonTag, blank=True, related_name="sermons")
    media_file = models.FileField(
        upload_to=sermon_audio_upload_path,
        validators=(validate_mp3,),
    )
    duration_seconds = models.PositiveIntegerField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-sermon_date", "-created_at")
        indexes = (
            models.Index(fields=("is_published", "sermon_date")),
            models.Index(fields=("collection", "sermon_date")),
        )

    def clean(self):
        super().clean()
        if self.is_published:
            missing = {
                field: _("This field is required before publishing.")
                for field in (
                    "title",
                    "speaker",
                    "sermon_date",
                    "summary",
                    "thesis",
                    "main_scripture",
                    "media_file",
                )
                if not getattr(self, field)
            }
            if missing:
                raise ValidationError(missing)
        if self.collection and not self.collection.is_published and self.is_published:
            raise ValidationError(
                {
                    "collection": _(
                        "A published sermon cannot use an unpublished collection."
                    )
                }
            )

    def save(self, *args, **kwargs):
        old_media_name = None
        if self.pk:
            old_media_name = (
                type(self).objects.filter(pk=self.pk)
                .values_list("media_file", flat=True)
                .first()
            )
        if not self.slug:
            base_slug = slugify(self.title) or "sermon"
            candidate = base_slug
            suffix = 2
            while type(self).objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        elif not self.is_published:
            self.published_at = None
        super().save(*args, **kwargs)
        if old_media_name and old_media_name != self.media_file.name:
            self._delete_media_name(old_media_name)

    def delete(self, *args, **kwargs):
        media_name = self.media_file.name
        result = super().delete(*args, **kwargs)
        if media_name:
            self._delete_media_name(media_name)
        return result

    def _delete_media_name(self, media_name):
        try:
            self.media_file.storage.delete(media_name)
        except Exception:
            logger.warning(
                "Unable to remove sermon media object %s for sermon %s.",
                media_name,
                self.pk,
                exc_info=True,
            )

    def __str__(self):
        return self.title
