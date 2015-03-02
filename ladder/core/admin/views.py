from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from authtools.views import LoginView

from ladder.core.decorators import AdminRequiredMixin

from ladder.apps.exchange.models import (
    TicketRequest,
    TicketOffer,
    TicketMatch,
)

User = get_user_model()


class AdminIndexView(AdminRequiredMixin, TemplateView):
    template_name = 'admin/index.html'

    def get_recent_users(self):
        return User.objects.order_by('-date_joined')[:10]

    def get_recent_requests(self):
        return TicketRequest.objects.order_by('-created_at')[:10]

    def get_recent_offers(self):
        return TicketOffer.objects.order_by('-created_at')[:10]

    def get_recent_matches(self):
        return TicketMatch.objects.order_by('-created_at')[:10]

    def get_exchange_metadata(self):
        meta = {
            'users': {
                'deactivated': User.objects.filter(is_active=False).count(),
                'active': User.objects.filter(is_active=True).count(),
                'total': User.objects.count(),
            },
            'requests': {
                'total': TicketRequest.objects.count(),
                'active': TicketRequest.objects.is_active().count(),
                'pending': TicketRequest.objects.is_reserved().count(),
                'fulfilled': TicketRequest.objects.is_fulfilled().count(),
                'cancelled': TicketRequest.objects.filter(is_cancelled=True).count(),
                'terminated': TicketRequest.objects.filter(is_terminated=True).count(),
            },
            'offers': {
                'total': TicketOffer.objects.count(),
                'active': TicketOffer.objects.is_active().count(),
                'pending': TicketOffer.objects.is_reserved().count(),
                'fulfilled': TicketOffer.objects.is_fulfilled().count(),
                'cancelled': TicketOffer.objects.filter(is_cancelled=True).count(),
                'terminated': TicketOffer.objects.filter(is_terminated=True).count(),
            },
            'matches': {
                'total': TicketMatch.objects.count(),
                'accepted': TicketMatch.objects.is_accepted().count(),
                'expired': TicketMatch.objects.is_expired().count(),
                'pending': TicketMatch.objects.is_awaiting_confirmation().count(),
                'terminated': TicketMatch.objects.is_terminated().count(),
                'cancelled': TicketMatch.objects.is_cancelled().count(),
            },
        }
        return meta

    def get_context_data(self, **kwargs):
        kwargs = super(AdminIndexView, self).get_context_data()
        kwargs['recently_registered_users'] = self.get_recent_users()
        kwargs['recent_requests'] = self.get_recent_requests()
        kwargs['recent_offers'] = self.get_recent_offers()
        kwargs['recent_matches'] = self.get_recent_matches()
        kwargs['exchange_meta'] = self.get_exchange_metadata()
        return kwargs


class AdminGuideView(AdminRequiredMixin, TemplateView):
    template_name = 'admin/guide.html'


class AdminLoginView(LoginView):
    disallow_authenticated = False
    template_name = 'admin/login.html'
    success_url = reverse_lazy('admin:index')

    def dispatch(self, *args, **kwargs):
        if getattr(self.request.user, 'is_admin', False):
            return redirect(self.get_success_url())
        return super(AdminLoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_admin:
            messages.error(
                self.request, 'This section of the site is only accessible to Admin users',
            )
            return self.form_invalid(form)
        return super(AdminLoginView, self).form_valid(form)
