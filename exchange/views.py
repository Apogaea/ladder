from django.views.generic.edit import FormView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from exchange.forms import TicketOfferForm, TicketRequestForm


class OfferTicketView(FormView):
    template_name = 'exchange/create_offer.html'
    form_class = TicketOfferForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.can_offer_ticket:
            raise PermissionDenied("User not eligable for ticket listing")
        return super(OfferTicketView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('dashboard')

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.user = self.request.user
        listing.save()
        messages.success(self.request, "Your listing has been created.")

        return super(OfferTicketView, self).form_valid(form)


offer_ticket = OfferTicketView.as_view()


class RequestTicketView(FormView):
    template_name = 'exchange/create_request.html'
    form_class = TicketRequestForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.can_request_ticket:
            raise PermissionDenied("User not eligable for ticket listing")
        return super(RequestTicketView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('dashboard')

    def form_valid(self, form):
        request = form.save(commit=False)
        request.user = self.request.user
        request.save()
        messages.success(self.request, "Your listing request has been created.")

        return super(RequestTicketView, self).form_valid(form)

request_ticket = RequestTicketView.as_view()
