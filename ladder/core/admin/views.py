from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from authtools.views import LoginView

from ladder.core.decorators import AdminRequiredMixin

User = get_user_model()


class AdminIndexView(AdminRequiredMixin, TemplateView):
    template_name = 'admin/index.html'

    def get_context_data(self, **kwargs):
        kwargs = super(AdminIndexView, self).get_context_data()
        kwargs['recently_registered_users'] = User.objects.order_by('-date_joined')[:10]
        return kwargs


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
