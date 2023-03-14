from django.apps import AppConfig


class ComposterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'composter'

    def ready(self):
        from . import signals  # noqa:F401
