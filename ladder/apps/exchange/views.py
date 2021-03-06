from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.utils import timezone
from django.core.urlresolvers import (
    reverse,
    reverse_lazy,
)

from authtools.views import LoginRequiredMixin

from ladder.apps.exchange.models import (
    TicketOffer,
    TicketRequest,
    TicketMatch
)
from ladder.apps.exchange.forms import (
    TicketOfferForm,
    TicketRequestForm,
    NoFieldsTicketOfferForm,
    NoFieldsTicketRequestForm,
    NoFieldsTicketMatchForm,
)
from ladder.apps.exchange.emails import (
    send_match_confirmation_email,
    send_request_fulfilled_email,
    send_offer_accepted_email,
)
from ladder.apps.exchange.mixins import (
    WithMatchMixin,
)


class OfferCreateView(LoginRequiredMixin, CreateView):
    template_name = 'exchange/offer_create.html'
    model = TicketOffer
    form_class = TicketOfferForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.can_offer_ticket:
            messages.error(self.request, "You may not create a new ticket offer")
            return redirect(reverse("dashboard"))
        return super(OfferCreateView, self).dispatch(request, *args, **kwargs)

    def get_front_of_request_line(self):
        """
        Fetch the first *front* of the ticket request line.
        """
        front_of_line = list(TicketRequest.objects.is_active().order_by(
            'created_at',
        )[:3])
        return front_of_line

    def get_context_data(self, **kwargs):
        context = super(OfferCreateView, self).get_context_data(**kwargs)
        context['ticket_request_choices'] = self.get_front_of_request_line()
        return context

    def create_match(self, ticket_offer=None, ticket_request=None):
        TicketMatch.objects.create_match(
            ticket_offer=ticket_offer,
            ticket_request=ticket_request,
            send_confirmation_email=True,
        )
        messages.success(
            self.request, "Your ticket offer has been matched with a ticket request.",
        )
        return redirect(self.get_success_url())

    def form_valid(self, form):
        self.object = ticket_offer = form.save(commit=False)
        ticket_offer.user = self.request.user
        ticket_offer.save()
        if form.cleaned_data.get('ticket_request'):
            ticket_request = form.cleaned_data['ticket_request']
            return self.create_match(ticket_offer, ticket_request)
        else:
            # Possible race condition here.  Two offers are created at almost
            # the same time.  Two matches will be created.
            try:
                return self.create_match(ticket_offer=ticket_offer)
            except TicketRequest.DoesNotExist:
                messages.success(
                    self.request,
                    "Your ticket offer has been created and will be "
                    "automatically matched to the next ticket request that "
                    "enters the system",
                )
            return redirect(self.get_success_url())


class OfferDetailView(LoginRequiredMixin, WithMatchMixin, DetailView):
    template_name = 'exchange/offer_detail.html'
    model = TicketOffer
    context_object_name = 'ticket_offer'

    def get_queryset(self):
        return self.request.user.ticket_offers.all().select_related().prefetch_related(
            'history', 'matches',
        )


class OfferCancelView(LoginRequiredMixin, UpdateView):
    template_name = 'exchange/offer_cancel.html'
    model = TicketOffer
    form_class = NoFieldsTicketOfferForm
    context_object_name = 'ticket_offer'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return self.request.user.ticket_offers.is_active()

    def form_valid(self, form):
        form.instance.is_cancelled = True
        form.save()
        messages.success(self.request, 'Your ticket offer has been cancelled')
        # See if there is a new match to be made.
        TicketMatch.objects.create_match(fail_silently=True, send_confirmation_email=True)
        return redirect(self.get_success_url())


class RequestCreateView(LoginRequiredMixin, CreateView):
    template_name = 'exchange/request_create.html'
    model = TicketRequest
    form_class = TicketRequestForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.can_request_ticket:
            messages.error(self.request, "You may not create a new ticket request.")
            return redirect(reverse("dashboard"))
        return super(RequestCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        ticket_request = form.save(commit=False)
        ticket_request.user = self.request.user
        ticket_request.save()
        # Possible race condition here.  Two requests are created at almost
        # the same time.  The same offer may be matched with two requests.
        try:
            ticket_match = TicketMatch.objects.create_match()
            if ticket_match.ticket_request == ticket_request:
                # mark it as accepted immediately.
                ticket_match.accepted_at = timezone.now()
                ticket_match.save()
                # send out the appropriate emails.
                send_offer_accepted_email(ticket_match, ticket_match.ticket_offer.user)
                send_request_fulfilled_email(ticket_match, ticket_match.ticket_request.user)
                messages.success(self.request, "Your request has been matched with a ticket.")
                return redirect(reverse('request-detail', kwargs={'pk': ticket_request.pk}))
            else:
                # If some other match was made, then send the confirmation
                # email.
                send_match_confirmation_email(ticket_match)
        except TicketOffer.DoesNotExist:
            pass
        finally:
            messages.success(
                self.request,
                "Your request has been created.  You will be notified as soon "
                "as we find a ticket for you.",
            )
        return redirect(ticket_request.get_absolute_url())


class RequestCancelView(LoginRequiredMixin, UpdateView):
    template_name = 'exchange/request_cancel.html'
    model = TicketRequest
    form_class = NoFieldsTicketRequestForm
    context_object_name = 'ticket_request'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return self.request.user.ticket_requests.is_active()

    def form_valid(self, form):
        form.instance.is_cancelled = True
        form.save()
        TicketMatch.objects.create_match(fail_silently=True, send_confirmation_email=True)
        messages.success(self.request, 'Your ticket request has been cancelled')
        return redirect(self.get_success_url())


class RequestDetailView(LoginRequiredMixin, WithMatchMixin, DetailView):
    template_name = 'exchange/request_detail.html'
    model = TicketRequest
    context_object_name = 'ticket_request'

    def get_queryset(self):
        return self.request.user.ticket_requests.all().select_related().prefetch_related(
            'history', 'matches',
        )


class MatchDetailView(LoginRequiredMixin, DetailView):
    template_name = 'exchange/match_detail.html'
    model = TicketMatch
    context_object_name = 'ticket_match'

    def get_queryset(self):
        return TicketMatch.objects.filter(
            Q(
                ticket_request__user=self.request.user,
            ) | Q(
                ticket_offer__user=self.request.user,
            )
        ).select_related()


class ConfirmTicketOfferView(LoginRequiredMixin, UpdateView):
    template_name = 'exchange/accept_ticket_offer.html'
    model = TicketMatch
    context_object_name = 'ticket_match'
    form_class = NoFieldsTicketMatchForm

    def get_success_url(self):
        return self.object.ticket_request.get_absolute_url()

    def get_queryset(self):
        return TicketMatch.objects.filter(
            ticket_request__user=self.request.user,
        ).is_awaiting_confirmation()

    def form_valid(self, form):
        if '_reject' in self.request.POST:
            ticket_request = form.instance.ticket_request
            ticket_request.is_cancelled = True
            ticket_request.save()
            TicketMatch.objects.create_match(fail_silently=True, send_confirmation_email=True)
            messages.info(
                self.request,
                'Your ticket request has been successfully cancelled.',
            )
            return redirect(reverse('dashboard'))
        else:
            messages.success(
                self.request,
                (
                    'You have successfully accepted your ticket.  Check your '
                    'email for information on how to get in touch with the '
                    'tickeholder.'
                ),
            )
            form.instance.accepted_at = timezone.now()
            match = form.save()
            # Send both users an email with info on how to get in touch with each other.
            send_offer_accepted_email(match, match.ticket_offer.user)
            send_request_fulfilled_email(match, match.ticket_request.user)
            return redirect(self.get_success_url())
