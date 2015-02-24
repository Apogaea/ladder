import json

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

    def create_match(self, ticket_offer, ticket_request):
        match = TicketMatch.objects.create(
            ticket_offer=ticket_offer,
            ticket_request=ticket_request,
        )
        # Send an email to the ticket requester with a confirmation link.
        send_match_confirmation_email(match)
        messages.success(
            self.request, "Your ticket offer has been matched with a ticket request.",
        )
        return redirect(self.get_success_url())

    def form_valid(self, form):
        self.object = ticket_offer = form.save(commit=False)
        ticket_offer.user = self.request.user
        ticket_offer.save()
        if ticket_offer.is_automatch:
            # Possible race condition here.  Two offers are created at almost
            # the same time.  Two matches will be created.
            try:
                ticket_request = TicketRequest.objects.is_active().order_by('created_at')[0]
                return self.create_match(ticket_offer, ticket_request)
            except IndexError:
                messages.success(
                    self.request,
                    "Your ticket offer has been created and will be "
                    "automatically matched to the next ticket request that "
                    "enters the system",
                )
            return redirect(self.get_success_url())
        elif form.cleaned_data.get('ticket_request'):
            ticket_request = form.cleaned_data['ticket_request']
            return self.create_match(ticket_offer, ticket_request)

        # Something weird happened, but lets just kick them back to the page.
        return self.form_invalid(form)


class OfferDetailView(LoginRequiredMixin, DetailView):
    template_name = 'exchange/offer_detail.html'
    model = TicketOffer
    context_object_name = 'ticket_offer'

    def get_queryset(self):
        return self.request.user.ticket_offers.all()

    def get_context_data(self, **kwargs):
        context = super(OfferDetailView, self).get_context_data(**kwargs)
        context['pending_match'] = self.object.get_pending_match()
        context['accepted_match'] = self.object.get_accepted_match()
        return context


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
        messages.success(self.request, 'Your ticket offer has been cancelled')
        return super(OfferCancelView, self).form_valid(form)


class RequestCreateView(LoginRequiredMixin, CreateView):
    template_name = 'exchange/request_form.html'
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
            ticket_offer = TicketOffer.objects.is_active().filter(
                is_automatch=True,
            ).order_by('created_at')[0]
            ticket_match = TicketMatch.objects.create(
                ticket_offer=ticket_offer,
                ticket_request=ticket_request,
            )
            messages.success(self.request, "Your request has been matched with a ticket.")
            return redirect(reverse('match-confirm', kwargs={'pk': ticket_match.pk}))
        except IndexError:
            messages.success(
                self.request,
                "Your request has been created.  You will be notified as soon "
                "as we find a ticket for you.",
            )
        return redirect(ticket_request.get_absolute_url())


class RequestUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'exchange/request_form.html'
    model = TicketRequest
    context_object_name = 'ticket_request'
    form_class = TicketRequestForm

    def get_queryset(self):
        return self.request.user.ticket_requests.is_active()

    def get_context_data(self, **kwargs):
        kwargs = super(RequestUpdateView, self).get_context_data(**kwargs)
        form = kwargs['form']
        message = form.data.get('message', self.get_object().message)
        kwargs['message_as_json'] = json.dumps(message)
        return kwargs


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
        messages.success(self.request, 'Your ticket request has been cancelled')
        return super(RequestCancelView, self).form_valid(form)


class RequestDetailView(LoginRequiredMixin, DetailView):
    template_name = 'exchange/request_detail.html'
    model = TicketRequest
    context_object_name = 'ticket_request'

    def get_queryset(self):
        return self.request.user.ticket_requests.all()

    def get_context_data(self, **kwargs):
        context = super(RequestDetailView, self).get_context_data(**kwargs)
        context['pending_match'] = self.object.get_pending_match()
        context['accepted_match'] = self.object.get_accepted_match()
        return context


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
        )


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
            form.instance.is_terminated = True
            form.instance.save()
            if TicketRequest.objects.is_active().exists():
                ticket_request = TicketRequest.objects.is_active().order_by('created_at')[0]
                new_match = TicketMatch.objects.create(
                    ticket_offer=form.instance.ticket_offer,
                    ticket_request=ticket_request,
                )
                # Send an email to the ticket requester with a confirmation link.
                send_match_confirmation_email(new_match)
            messages.info(self.request, 'Your ticket request has been successfully cancelled.')
            return redirect(reverse('dashboard'))
        else:
            messages.info(self.request, 'You have successfully accepted the offered ticket.')
            form.instance.accepted_at = timezone.now()
            match = form.save()
            # Send both users an email with info on how to get in touch with each other.
            send_offer_accepted_email(match, match.ticket_offer.user)
            send_request_fulfilled_email(match, match.ticket_request.user)
            return redirect(self.get_success_url())
