from django.apps import AppConfig


class StylesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'styles'

    def ready(self):
        from django.db.models.signals import post_save, post_delete
        from . import signals
        from .models import Style

        post_save.connect(signals.styles_changed, sender=Style)
        post_delete.connect(signals.styles_deleted, sender=Style)
