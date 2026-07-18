from django.apps import AppConfig


class ContentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "content"

    def ready(self):
        # Register signal handlers (email notifications on new comments).
        from . import signals  # noqa: F401
