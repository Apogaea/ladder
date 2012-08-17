from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from fusionbox.http import HttpResponseSeeOther

from exchange.models import TicketListing, TicketRequest
from exchange.forms import TicketListingForm, TicketRequestForm


class CreateListingView(CreateView):
    template_name = 'exchange/listing_create.html'
    model = TicketListing
    form_class = TicketListingForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.can_list_ticket:
            raise PermissionDenied("User not eligable for ticket listing")
        return super(CreateListingView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateListingView, self).get_context_data(**kwargs)
        context['radios'] = dict([(r.choice_value, r.choice_label) for r in context['form']['type']])
        return context

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.user = self.request.user
        listing.save()
        messages.success(self.request, "Your listing has been created.")

        return HttpResponseSeeOther(listing.get_absolute_url())

listing_create = CreateListingView.as_view()


class ListingDetailView(DetailView):
    template_name = 'exchange/listing_detail.html'
    model = TicketListing
    context_object_name = 'listing'

    def get_queryset(self):
        return self.request.user.listings.all()

listing_detail = ListingDetailView.as_view()


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
    model = TicketListing
    context_object_name = 'listing'

    def get_queryset(self):
        return self.request.user.requests.active()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset)

request_detail = RequestDetailView.as_view()
