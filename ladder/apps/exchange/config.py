from django.apps import AppConfig
from django import dispatch
from django.db.models.signals import (
    pre_save,
    post_save,
)


class ExchangeConfig(AppConfig):
    name = 'ladder.apps.exchange'
    label = 'exchange'
    verbose_name = 'Exchange'

    def ready(self):
        # Signals
        from ladder.apps.exchange.receivers import (
            create_creation_history_entry,
            create_cancellation_history_entry,
            create_termination_history_entry,
            create_match_creation_history_entries,
            create_match_confirmation_history_entries,
        )
        dispatch.receiver(post_save, sender='exchange.TicketRequest')(
            create_creation_history_entry,
        )
        dispatch.receiver(post_save, sender='exchange.TicketOffer')(
            create_creation_history_entry,
        )
        dispatch.receiver(pre_save, sender='exchange.TicketRequest')(
            create_cancellation_history_entry,
        )
        dispatch.receiver(pre_save, sender='exchange.TicketOffer')(
            create_cancellation_history_entry,
        )
        dispatch.receiver(pre_save, sender='exchange.TicketRequest')(
            create_termination_history_entry,
        )
        dispatch.receiver(pre_save, sender='exchange.TicketOffer')(
            create_termination_history_entry,
        )
        dispatch.receiver(post_save, sender='exchange.TicketMatch')(
            create_match_creation_history_entries,
        )
        dispatch.receiver(pre_save, sender='exchange.TicketMatch')(
            create_match_confirmation_history_entries,
        )
