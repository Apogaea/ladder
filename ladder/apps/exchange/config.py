from django.apps import AppConfig
from django import dispatch
from django.db.models.signals import post_save
from django.conf import settings


class ExchangeConfig(AppConfig):
    name = 'ladder.apps.exchange'
    label = 'exchange'
    verbose_name = 'Exchange'

    def ready(self):
        # Signals
        from ladder.apps.exchange.receivers import create_ladder_profile

        dispatch.receiver(post_save, sender=settings.AUTH_USER_MODEL)(
            create_ladder_profile,
        )
