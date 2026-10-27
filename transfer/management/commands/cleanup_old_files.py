
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from transfer.models import SharedFile


class Command(BaseCommand):
    help = "Menghapus file yang sudah berusia 10 menit"

    def handle(self, *args, **options):
        batas_waktu = timezone.now() - timedelta(minutes=1)

        files = SharedFile.objects.filter(
            uploaded_at__lt=batas_waktu
        )

        jumlah = files.count()

        for item in files:
            item.file.delete(save=False)
            item.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Berhasil menghapus {jumlah} file lama."
            )
        )
