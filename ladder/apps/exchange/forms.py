from django import forms

from betterforms.forms import (
    BetterModelForm,
    BetterForm,
)

from ladder.apps.exchange.models import (
    TicketOffer, TicketRequest, TicketMatch,
)


class TicketOfferForm(BetterModelForm):
    """
    Form for creating a ticket offer.
    """
    ticket_request = forms.IntegerField(required=False)

    class Meta:
        model = TicketOffer
        fields = ('is_automatch',)

    def clean_ticket_request(self):
        ticket_request_pk = self.cleaned_data.get('ticket_request')
        if ticket_request_pk is None:
            return
        try:
            ticket_request = TicketRequest.objects.is_active().get(pk=ticket_request_pk)
            place_in_line = ticket_request.place_in_line
            if place_in_line is None:
                raise forms.ValidationError("Invalid ticket request")
            elif place_in_line >= 3:
                raise forms.ValidationError("Invalid ticket request")
            return ticket_request
        except TicketRequest.DoesNotExist:
            raise forms.ValidationError("Invalid or unknown ticket request id")


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
