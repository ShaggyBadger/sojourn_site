import hashlib
import io
import logging
import os
import unicodedata
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import get_valid_filename
from django.utils.translation import gettext_lazy as _
from PIL import Image

from .validators import validate_image_upload


logger = logging.getLogger(__name__)


def media_asset_upload_path(instance, filename):
    """Store public assets under a non-colliding, dedicated storage prefix."""
    extension = os.path.splitext(filename)[1].lower() or ".bin"
    return f"media/assets/{uuid.uuid4().hex}{extension}"


def normalize_tag_name(value):
    """Return the canonical form used to enforce case-insensitive tag uniqueness."""
    normalized = unicodedata.normalize("NFKC", value or "")
    return " ".join(normalized.split()).casefold()


def _record_cleanup_issue(storage_key, reason, error=""):
    """Record a cleanup failure without masking the original media operation."""
    try:
        MediaCleanupIssue.objects.create(
            storage_key=storage_key,
            reason=reason,
            last_error=str(error)[:2_000],
        )
    except Exception:
        logger.error(
            "Unable to record media cleanup issue for %s.",
            storage_key,
            exc_info=True,
        )


class MediaTag(models.Model):
    """Reusable staff-facing tag for organizing media assets."""

    name = models.CharField(max_length=100)
    normalized_name = models.CharField(max_length=100, unique=True, editable=False)

    class Meta:
        ordering = ("name",)
        verbose_name = "media tag"
        verbose_name_plural = "media tags"

    def clean(self):
        super().clean()
        self.name = " ".join((self.name or "").split())
        if not self.name:
            raise ValidationError({"name": _("Enter a tag name.")})
        self.normalized_name = normalize_tag_name(self.name)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MediaAsset(models.Model):
    """A reusable public website asset managed through Django admin."""

    class MediaType(models.TextChoices):
        IMAGE = "image", "Image"

    class StorageStatus(models.TextChoices):
        PRESENT = "present", "Present"
        MISSING = "missing", "Missing"
        UNVERIFIED = "unverified", "Unverified"

    file = models.FileField(
        upload_to=media_asset_upload_path,
        validators=(validate_image_upload,),
    )
    name = models.CharField(max_length=255)
    original_filename = models.CharField(max_length=255, editable=False)
    description = models.TextField(blank=True)
    alt_text_en = models.CharField(
        blank=True,
        help_text="Default English alternative text; placements may override it.",
        max_length=255,
    )
    alt_text_es = models.CharField(
        blank=True,
        help_text="Optional Spanish default alternative text.",
        max_length=255,
    )
    media_type = models.CharField(
        choices=MediaType.choices,
        default=MediaType.IMAGE,
        max_length=20,
    )
    tags = models.ManyToManyField(MediaTag, blank=True, related_name="assets")
    mime_type = models.CharField(max_length=100, editable=False, blank=True)
    file_size = models.PositiveBigIntegerField(default=0, editable=False)
    width = models.PositiveIntegerField(blank=True, null=True, editable=False)
    height = models.PositiveIntegerField(blank=True, null=True, editable=False)
    sha256 = models.CharField(max_length=64, editable=False, blank=True)
    storage_status = models.CharField(
        choices=StorageStatus.choices,
        default=StorageStatus.UNVERIFIED,
        max_length=12,
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="uploaded_media_assets",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", "name")
        verbose_name = "media asset"
        verbose_name_plural = "media assets"

    def clean(self):
        super().clean()
        if self.media_type != self.MediaType.IMAGE:
            raise ValidationError({"media_type": _("Only image assets are supported currently.")})
        if self.file and getattr(self.file, "_file", None):
            validate_image_upload(self.file.file)

    def _prepare_uploaded_file(self):
        """Validate and strip image metadata before a new upload reaches storage."""
        if not self.file or not getattr(self.file, "_file", None):
            return

        uploaded_file = self.file.file
        validate_image_upload(uploaded_file)
        extension = os.path.splitext(uploaded_file.name)[1].lower()
        uploaded_file.seek(0)
        with Image.open(uploaded_file) as image:
            output = io.BytesIO()
            image_format = image.format
            save_kwargs = {"format": image_format}
            if image_format == "JPEG":
                if image.mode not in {"RGB", "L", "CMYK"}:
                    image = image.convert("RGB")
                save_kwargs.update(quality=95, optimize=True)
            elif image_format == "PNG":
                save_kwargs.update(optimize=True)
            image.save(output, **save_kwargs)
            output.seek(0)
        self.file = ContentFile(output.read(), name=get_valid_filename(os.path.basename(uploaded_file.name)))
        self.file.name = f"upload{extension}"

    def _populate_metadata(self, original_filename):
        """Populate searchable file metadata from the uploaded content."""
        self.original_filename = original_filename
        self.file_size = self.file.size
        self.sha256 = hashlib.sha256()
        self.file.open("rb")
        try:
            for chunk in iter(lambda: self.file.read(1024 * 1024), b""):
                self.sha256.update(chunk)
            self.sha256 = self.sha256.hexdigest()
            self.file.seek(0)
            with Image.open(self.file) as image:
                self.width = image.width
                self.height = image.height
                self.mime_type = Image.MIME.get(image.format, "")
        finally:
            self.file.close()

    def save(self, *args, **kwargs):
        """Validate, sanitize, and persist an asset with failure-aware cleanup."""
        is_new_upload = bool(self.file and getattr(self.file, "_file", None))
        old_name = None
        original_filename = None
        if self.pk:
            old_name = type(self).objects.filter(pk=self.pk).values_list("file", flat=True).first()
        if is_new_upload:
            original_filename = get_valid_filename(os.path.basename(self.file.name))[:255]
            self._prepare_uploaded_file()
            self._populate_metadata(original_filename)
            self.storage_status = self.StorageStatus.PRESENT
        if is_new_upload:
            self.full_clean()
        else:
            self.full_clean(exclude=("file",))
        new_name = None
        try:
            result = super().save(*args, **kwargs)
            new_name = self.file.name
        except Exception as error:
            if is_new_upload and self.file.name:
                try:
                    self.file.storage.delete(self.file.name)
                except Exception as cleanup_error:
                    _record_cleanup_issue(self.file.name, "database save failed", cleanup_error)
            raise
        if old_name and old_name != new_name:
            try:
                self.file.storage.delete(old_name)
            except Exception as error:
                logger.warning("Unable to remove replaced media object %s.", old_name, exc_info=True)
                _record_cleanup_issue(old_name, "asset replacement cleanup failed", error)
        return result

    def delete(self, *args, **kwargs):
        """Delete the database record and then its unreferenced storage object."""
        storage_name = self.file.name
        storage = self.file.storage
        result = super().delete(*args, **kwargs)
        if storage_name:
            try:
                storage.delete(storage_name)
            except Exception as error:
                logger.warning("Unable to remove media object %s.", storage_name, exc_info=True)
                _record_cleanup_issue(storage_name, "asset deletion cleanup failed", error)
        return result

    def __str__(self):
        return self.name


class MediaCleanupIssue(models.Model):
    """A storage object that needs a retry after lifecycle cleanup failed."""

    storage_key = models.CharField(max_length=512)
    reason = models.CharField(max_length=255)
    last_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "media cleanup issue"
        verbose_name_plural = "media cleanup issues"

    def __str__(self):
        return f"{self.storage_key} ({self.reason})"
