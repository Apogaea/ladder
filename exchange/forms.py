from django import forms

from ladder.forms import CssModelForm

from exchange.models import TicketListing, TicketRequest


class TicketListingForm(CssModelForm):
    class Meta:
        model = TicketListing
        fields = ('type',)
        widgets = {
                'type': forms.RadioSelect(),
                }


class TicketRequestForm(CssModelForm):
    class Meta:
        model = TicketRequest
        fields = ('message',)
