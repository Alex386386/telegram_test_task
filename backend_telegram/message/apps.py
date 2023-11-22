from django.apps import AppConfig
from django.db.models.signals import post_migrate


class MessageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'message'

    def ready(self):
        post_migrate.connect(run_on_startup, sender=self)


def run_on_startup(sender, **kwargs):
    from .tasks import fetch_and_update_currency_rates
    fetch_and_update_currency_rates()
