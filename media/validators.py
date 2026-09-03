import os

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from PIL import Image, UnidentifiedImageError


MAX_MEDIA_FILE_SIZE = 10 * 1024 * 1024
MAX_IMAGE_DIMENSION = 8_000
MAX_IMAGE_PIXELS = 40_000_000
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_IMAGE_FORMATS_BY_EXTENSION = {
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".png": "PNG",
    ".webp": "WEBP",
}


def validate_image_upload(uploaded_file):
    """Validate an uploaded image by size, extension, and decoded contents."""
    if uploaded_file.size > MAX_MEDIA_FILE_SIZE:
        raise ValidationError(_("Images must be 10 MiB or smaller."))

    extension = os.path.splitext(uploaded_file.name)[1].lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(_("Upload a JPEG, PNG, or WebP image."))

    content_type = getattr(uploaded_file, "content_type", None)
    expected_content_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }
    if content_type and content_type != expected_content_types[extension]:
        raise ValidationError(_("The image content type does not match its extension."))

    try:
        uploaded_file.seek(0)
        with Image.open(uploaded_file) as image:
            if image.format != ALLOWED_IMAGE_FORMATS_BY_EXTENSION[extension]:
                raise ValidationError(_("Upload a JPEG, PNG, or WebP image."))
            if image.width > MAX_IMAGE_DIMENSION or image.height > MAX_IMAGE_DIMENSION:
                raise ValidationError(_("Images must be 8,000 pixels or smaller in either dimension."))
            if image.width * image.height > MAX_IMAGE_PIXELS:
                raise ValidationError(_("Images must contain 40 million pixels or fewer."))
            if getattr(image, "n_frames", 1) > 1:
                raise ValidationError(_("Animated images are not supported."))
            image.verify()
    except UnidentifiedImageError as error:
        raise ValidationError(_("The uploaded file is not a valid image.")) from error
    finally:
        uploaded_file.seek(0)
