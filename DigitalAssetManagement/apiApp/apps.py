from django.apps import AppConfig
import uuid

class ApiappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apiApp"

    def ready(self):
        import apiApp.signals