from django import forms

from betterforms.forms import BetterModelForm, BetterForm

from exchange.models import (
    TicketOffer, TicketRequest, TicketMatch,
)


class TicketOfferForm(BetterModelForm):
    """
    Form for creating a ticket offer.
    """
    class Meta:
        model = TicketOffer
        fields = ('is_automatch',)


class TicketRequestForm(BetterModelForm):
    """
    Form for creating a ticket request.
    """
    class Meta:
        model = TicketRequest
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'ng-model': 'message'}),
        }


class SelectTicketRequestForm(BetterForm):
    """
    Form for presenting a user with a choice of ticket requests to fulfill.
    """
    ticket_request = forms.ModelChoiceField(queryset=TicketRequest.objects.none())


class NoFieldsTicketOfferForm(BetterModelForm):
    class Meta:
        model = TicketMatch
        fields = tuple()


class NoFieldsTicketRequestForm(BetterModelForm):
    class Meta:
        model = TicketRequest
        fields = tuple()


class NoFieldsTicketMatchForm(BetterModelForm):
    class Meta:
        model = TicketMatch
        fields = tuple()
