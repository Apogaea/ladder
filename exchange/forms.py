from django import forms

from ladder.forms import CssModelForm

from exchange.models import TicketOffer, TicketRequest


class TicketOfferForm(CssModelForm):
    class Meta:
        model = TicketOffer
        fields = ('type',)
        widgets = {
                'type': forms.RadioSelect(),
                }


class TicketRequestForm(CssModelForm):
    class Meta:
        model = TicketRequest
        fields = tuple()
