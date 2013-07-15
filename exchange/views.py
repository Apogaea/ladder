from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from fusionbox.http import HttpResponseSeeOther

from authtools.views import LoginRequired

from exchange.models import TicketOffer, TicketRequest
from exchange.forms import TicketOfferForm, TicketRequestForm


class CreateOfferView(LoginRequired, CreateView):
    template_name = 'exchange/offer_create.html'
    model = TicketOffer
    form_class = TicketOfferForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.can_list_ticket:
            raise PermissionDenied("User not eligable for ticket listing")
        return super(CreateOfferView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('exchange.views.offer_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.user = self.request.user
        listing.save()
        # TODO: auto match if `is_automatch`
        messages.success(self.request, "Your listing has been created.")

        return HttpResponseSeeOther(listing.get_absolute_url())

offer_create = CreateOfferView.as_view()


class OfferDetailView(DetailView):
    template_name = 'exchange/listing_detail.html'
    model = TicketOffer
    context_object_name = 'listing'

    def get_queryset(self):
        return self.request.user.listings.all()

listing_detail = OfferDetailView.as_view()


class RequestTicketView(CreateView):
    template_name = 'exchange/request_create.html'
    model = TicketRequest
    form_class = TicketRequestForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.can_request_ticket:
            raise PermissionDenied("User not eligable for ticket listing")
        return super(RequestTicketView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = form.save(commit=False)
        request.user = self.request.user
        request.save()
        messages.success(self.request, "Your listing request has been created.")

        return HttpResponseSeeOther(request.get_absolute_url())

request_create = RequestTicketView.as_view()


class RequestDetailView(DetailView):
    template_name = 'exchange/request_detail.html'
    model = TicketRequest
    context_object_name = 'ticket_request'

    def get_queryset(self):
        return self.request.user.requests.active()

request_detail = RequestDetailView.as_view()
