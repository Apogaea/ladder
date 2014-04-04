from betterforms.changelist import SearchForm

from exchange.models import TicketOffer, TicketRequest, TicketMatch


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
