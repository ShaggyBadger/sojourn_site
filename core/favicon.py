"""Favicon-specific image preparation for site settings."""

from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

from media.models import MediaAsset


FAVICON_SIZE = 512


def _is_valid_favicon(asset):
    return (
        asset.mime_type == "image/png"
        and asset.width == asset.height
        and asset.width is not None
        and 16 <= asset.width <= FAVICON_SIZE
    )


def prepare_favicon_asset(asset):
    """Return a valid favicon asset, creating a centered PNG derivative if needed."""
    if _is_valid_favicon(asset):
        return asset

    if asset.storage_status == MediaAsset.StorageStatus.MISSING or not asset.file.name:
        return asset

    asset.file.open("rb")
    try:
        with Image.open(asset.file) as image:
            favicon = ImageOps.fit(
                image.convert("RGBA"),
                (FAVICON_SIZE, FAVICON_SIZE),
                method=Image.Resampling.LANCZOS,
            )
            output = BytesIO()
            favicon.save(output, format="PNG", optimize=True)
    finally:
        asset.file.close()

    derivative = MediaAsset(
        file=ContentFile(output.getvalue(), name="favicon.png"),
        name=f"{asset.name} (favicon)",
        description=f"Automatically generated favicon from media asset {asset.pk}.",
        alt_text_en=asset.alt_text_en,
        alt_text_es=asset.alt_text_es,
    )
    derivative.save()
    return derivative
