from django.views.generic.edit import FormView
from django.contrib import messages
from django.views.generic.base import TemplateView, RedirectView
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

from accounts.forms import UserForm, PhoneVerificationForm
from accounts.models import PhoneVerification


class ProtectedView(TemplateView):
    """
    Enforces login required on all views dispatched by this view
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)


class DashboardView(ProtectedView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        if not self.request.user.phone_number:
            context['phone_form'] = UserForm(instance=self.request.user)
        return context

dashboard = DashboardView.as_view()


class EditAccountView(FormView):
    template_name = 'accounts/account_edit.html'
    form_class = UserForm
    success_url = reverse_lazy('dashboard')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditAccountView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditAccountView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Your profile was successfully updated")
        if not user.is_verified and not user.codes.active().exists():
            code = PhoneVerification.objects.create(user=user)
            if code.can_send:
                code.send()
            messages.info(self.request, "An account verification code has been sent to {0}.".format(code.phone_number))
            return HttpResponseRedirect(reverse('account_verify'))
        return super(EditAccountView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating your profile.  Please correct the errors below")
        return super(EditAccountView, self).form_invalid(form)


account_edit = EditAccountView.as_view()


class SendCodeView(RedirectView):
    permanent = False
    query_string = False

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.can_send_code))
    def dispatch(self, *args, **kwargs):
        return super(SendCodeView, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, **kwargs):
        code = self.request.user.codes.latest('-sent_at')
        if code.can_send:
            code.send()
            messages.success(self.request, "An account verification code has been sent to {0}.".format(code.phone_number))
        return self.request.GET.get('next', reverse('account_verify'))

account_send_verification_code = SendCodeView.as_view()


class VerifyPhoneView(FormView):
    template_name = 'accounts/account_verify.html'
    form_class = PhoneVerificationForm
    success_url = reverse_lazy('dashboard')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_verified:
            raise PermissionDenied("Resending verification code too soon")
        return super(VerifyPhoneView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(VerifyPhoneView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        code = form.cleaned_data.get('verification_code')
        user = form.user
        if user.validate(code):
            messages.success(self.request, "Your account is now verified.")
            return super(VerifyPhoneView, self).form_valid(form)
        else:
            messages.error(self.request, "The verification code entered did not match")
            return super(VerifyPhoneView, self).form_invalid(form)


account_verify = VerifyPhoneView.as_view()
