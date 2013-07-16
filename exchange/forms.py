from django import forms
from django.utils import timezone

from fusionbox.forms import BaseModelForm, BaseForm

from exchange.models import TicketOffer, TicketRequest, TicketMatch


class TicketOfferForm(BaseModelForm):
    """
    Form for creating a ticket offer.
    """
    class Meta:
        model = TicketOffer
        fields = ('is_automatch',)


class TicketRequestForm(BaseModelForm):
    """
    Form for creating a ticket request.
    """
    class Meta:
        model = TicketRequest
        fields = ('message',)


class SelectTicketRequestForm(BaseForm):
    """
    Form for presenting a user with a choice of ticket requests to fulfill.
    """
    ticket_request = forms.ModelChoiceField(queryset=TicketRequest.objects.none())


class AcceptTicketOfferForm(BaseModelForm):
    """
    This form marks a ticket match as accepted when saved.
    """
    class Meta:
        model = TicketMatch
        fields = tuple()

    def save(self, *args, **kwargs):
        self.instance.accepted_at = timezone.now()
        super(AcceptTicketOfferForm, self).save(*args, **kwargs)
