from django.apps import AppConfig
import os


# class TransferConfig(AppConfig):
#     name = 'transfer'

class TransferConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "transfer"

    def ready(self):
        # Jalankan hanya pada proses utama runserver
        # yang menggunakan autoreloader Django.
        if os.environ.get("RUN_MAIN") != "true":
            return

        from .cleanup import start_cleanup_thread

        start_cleanup_thread()
