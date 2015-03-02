from django import forms

from betterforms.forms import (
    BetterModelForm,
)
from betterforms.changelist import SearchForm

from ladder.apps.exchange.models import (
    TicketOffer,
    TicketRequest,
    TicketMatch,
)


class OfferChangeListForm(SearchForm):
    SEARCH_FIELDS = ('user__email', 'user__display_name')
    model = TicketOffer


class RequestChangeListForm(SearchForm):
    SEARCH_FIELDS = ('user__email', 'user__display_name')
    model = TicketRequest


class MatchChangeListForm(SearchForm):
    SEARCH_FIELDS = (
        'ticket__request__user__email',
        'ticket__request__user__display_name',
        'ticket__offer__user__email',
        'ticket__offer__user__display_name',
    )
    model = TicketMatch


class TicketMatchTerminationForm(BetterModelForm):
    terminate_request = forms.BooleanField(required=False)
    terminate_offer = forms.BooleanField(required=False)

    def clean(self):
        cd = super(TicketMatchTerminationForm, self).clean()
        terminate_request = cd.get('terminate_request')
        terminate_offer = cd.get('terminate_offer')
        if not terminate_request and not terminate_offer:
            raise forms.ValidationError("Must choose either offer or request to be terminate")
        return cd

    class Meta:
        model = TicketMatch
        fields = tuple()
