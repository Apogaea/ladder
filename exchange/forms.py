from django import forms

from fusionbox.forms import BaseModelForm

from exchange.models import TicketOffer, TicketRequest


class TicketOfferForm(BaseModelForm):
    class Meta:
        model = TicketOffer
        fields = ('is_automatch',)


class TicketRequestForm(BaseModelForm):
    class Meta:
        model = TicketRequest
        fields = ('message',)
