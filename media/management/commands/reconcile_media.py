import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from media.models import MediaAsset, MediaCleanupIssue


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Reconcile media storage status and retry failed object cleanup."

    def handle(self, *args, **options):
        self._check_assets()
        self._retry_cleanup()

    def _check_assets(self):
        for asset in MediaAsset.objects.exclude(file=""):
            try:
                exists = asset.file.storage.exists(asset.file.name)
            except Exception:
                logger.warning("Unable to verify media object %s.", asset.file.name, exc_info=True)
                continue
            status = (
                MediaAsset.StorageStatus.PRESENT
                if exists
                else MediaAsset.StorageStatus.MISSING
            )
            if asset.storage_status != status:
                asset.storage_status = status
                asset.save(update_fields=("storage_status", "updated_at"))
            self.stdout.write(f"{asset.pk}: {status}")

    def _retry_cleanup(self):
        storage = MediaAsset.file.field.storage
        for issue in MediaCleanupIssue.objects.filter(resolved_at__isnull=True):
            try:
                storage.delete(issue.storage_key)
            except Exception as error:
                issue.last_error = str(error)[:2_000]
                issue.save(update_fields=("last_error",))
                logger.warning("Unable to reconcile media object %s.", issue.storage_key, exc_info=True)
                self.stdout.write(self.style.WARNING(f"Still unresolved: {issue.storage_key}"))
                continue
            issue.resolved_at = timezone.now()
            issue.save(update_fields=("resolved_at",))
            self.stdout.write(self.style.SUCCESS(f"Resolved: {issue.storage_key}"))
