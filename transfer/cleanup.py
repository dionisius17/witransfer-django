
import logging
import threading
import time
from datetime import timedelta

from django.utils import timezone

logger = logging.getLogger(__name__)

_cleanup_started = False


def delete_old_files():
    from .models import SharedFile

    batas_waktu = timezone.now() - timedelta(minutes=2)

    files = SharedFile.objects.filter(
        uploaded_at__lt=batas_waktu
    )

    for item in files.iterator():
        try:
            item.file.delete(save=False)
            item.delete()
            logger.info("File lama berhasil dihapus.")
        except Exception:
            logger.exception("Gagal menghapus file lama.")


def start_cleanup_thread():
    global _cleanup_started

    if _cleanup_started:
        return

    _cleanup_started = True

    def worker():
        while True:
            time.sleep(60)

            try:
                delete_old_files()
            except Exception:
                logger.exception("Pemeriksaan file lama gagal.")

    thread = threading.Thread(
        target=worker,
        daemon=True,
        name="localshare-cleanup",
    )
    thread.start()
