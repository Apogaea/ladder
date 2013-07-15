from django.views.generic import FormView, CreateView, TemplateView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

from authtools.views import LoginRequiredMixin

from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import User


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

dashboard = DashboardView.as_view()


class EditAccountView(LoginRequiredMixin, FormView):
    template_name = 'accounts/account_edit.html'
    form_class = UserChangeForm
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


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('register_success')

register = RegisterView.as_view()


class RegistrationSuccess(TemplateView):
    template_name = 'accounts/register_success.html'

register_success = RegistrationSuccess.as_view()
