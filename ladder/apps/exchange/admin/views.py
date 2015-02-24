from django.views.generic import DetailView, UpdateView
from django.forms.models import modelform_factory
from django.conf import settings
from django.core.urlresolvers import reverse

from betterforms.views import BrowseView

from ladder.core.decorators import AdminRequiredMixin

from ladder.apps.exchange.models import (
    TicketOffer,
    TicketRequest,
    TicketMatch,
)
from ladder.apps.exchange.admin.forms import (
    OfferChangeListForm,
    RequestChangeListForm,
    MatchChangeListForm,
)


#
# Ticket Offer Admin
#
class AdminOfferListView(AdminRequiredMixin, BrowseView):
    template_name = 'exchange/admin/offer_list.html'
    model = TicketOffer
    form_class = OfferChangeListForm
    paginate_by = settings.PAGINATE_BY


class AdminOfferDetailView(AdminRequiredMixin, DetailView):
    template_name = 'exchange/admin/offer_detail.html'
    model = TicketOffer
    context_object_name = 'ticket_offer'


class AdminOfferToggleTerminateView(AdminRequiredMixin, UpdateView):
    template_name = 'exchange/admin/offer_terminate.html'
    model = TicketOffer
    context_object_name = 'ticket_offer'
    form_class = modelform_factory(TicketOffer, fields=[])

    def form_valid(self, form):
        form.instance.is_terminated = not form.instance.is_terminated
        return super(AdminOfferToggleTerminateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin:offer-detail', kwargs={'pk': self.object.pk})


#
# Ticket Request Admin
#
class AdminRequestListView(AdminRequiredMixin, BrowseView):
    template_name = 'exchange/admin/request_list.html'
    model = TicketRequest
    form_class = RequestChangeListForm
    paginate_by = settings.PAGINATE_BY


class AdminRequestDetailView(AdminRequiredMixin, DetailView):
    template_name = 'exchange/admin/request_detail.html'
    model = TicketRequest
    context_object_name = 'ticket_request'


class AdminRequestToggleTerminateView(AdminRequiredMixin, UpdateView):
    template_name = 'exchange/admin/request_terminate.html'
    model = TicketRequest
    context_object_name = 'ticket_request'
    form_class = modelform_factory(TicketRequest, fields=[])

    def form_valid(self, form):
        form.instance.is_terminated = not form.instance.is_terminated
        return super(AdminRequestToggleTerminateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin:request-detail', kwargs={'pk': self.object.pk})


#
# Ticket Match Admin
#
class AdminMatchListView(AdminRequiredMixin, BrowseView):
    template_name = 'exchange/admin/match_list.html'
    model = TicketMatch
    form_class = MatchChangeListForm
    paginate_by = settings.PAGINATE_BY


class AdminMatchDetailView(AdminRequiredMixin, DetailView):
    template_name = 'exchange/admin/match_detail.html'
    model = TicketMatch
    context_object_name = 'ticket_match'


class AdminMatchToggleTerminateView(AdminRequiredMixin, UpdateView):
    template_name = 'exchange/admin/match_terminate.html'
    model = TicketMatch
    context_object_name = 'ticket_match'
    form_class = modelform_factory(TicketMatch, fields=[])

    def form_valid(self, form):
        form.instance.is_terminated = not form.instance.is_terminated
        return super(AdminMatchToggleTerminateView, self).form_valid(form)
