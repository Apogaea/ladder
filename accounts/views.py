from django.views.generic.edit import FormView
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from accounts.forms import NewUserForm


class ProtectedView(TemplateView):
    """
    Enforces login required on all views dispatched by this view
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)


class DashboardView(ProtectedView):
    template_name = 'accounts/dashboard.html'


dashboard = DashboardView.as_view()


class EditAccountView(FormView):
    template_name = 'accounts/account_edit.html'
    form_class = NewUserForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FormView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditAccountView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user

        return kwargs

    def get_success_url(self):
        return reverse('dashboard')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your profile has been successfully updated")
        return super(EditAccountView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating your profile.  Please correct the errors below")
        return super(EditAccountView, self).form_invalid(form)


account_edit = EditAccountView.as_view()
