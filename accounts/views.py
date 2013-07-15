from django.views.generic.edit import FormView
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy

from accounts.forms import UserForm

from authtools.views import LoginRequired


class DashboardView(LoginRequired, TemplateView):
    template_name = 'accounts/dashboard.html'

dashboard = DashboardView.as_view()


class EditAccountView(LoginRequired, FormView):
    template_name = 'accounts/account_edit.html'
    form_class = UserForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super(EditAccountView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Your profile was successfully updated")
        return super(EditAccountView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating your profile.  Please correct the errors below")
        return super(EditAccountView, self).form_invalid(form)


account_edit = EditAccountView.as_view()
