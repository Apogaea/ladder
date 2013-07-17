from django.views.generic import FormView, CreateView, TemplateView
from django.contrib import auth
from django.contrib import messages
from django.utils.http import base36_to_int
from django.contrib.auth.forms import SetPasswordForm
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.tokens import default_token_generator as token_generator

from authtools.views import LoginRequiredMixin

from exchange.forms import PhoneNumberForm

from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import User
from accounts.emails import send_registration_verification_email


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        kwargs = super(DashboardView, self).get_context_data(**kwargs)
        if not self.request.user.ladder_profile.phone_numbers.exists():
            kwargs['phone_number_form'] = PhoneNumberForm()
        return kwargs

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

    def form_valid(self, form):
        self.object = user = form.save()
        send_registration_verification_email(user)
        return redirect(self.get_success_url())

register = RegisterView.as_view()


class RegistrationSuccessView(TemplateView):
    template_name = 'accounts/register_success.html'

register_success = RegistrationSuccessView.as_view()


class VerifyEmailView(FormView):
    """
    Base view for clients and fitters to confirm their relationship to a
    business.  Checks that the token in the URL corresponds correctly to the
    relationship, and presents the user with an accept/reject form.
    """
    form_class = SetPasswordForm
    template_name = 'accounts/verify_email_confirm.html'

    def get_success_url(self, **kwargs):
        # TODO: redirect to enter phone number view.
        return reverse('dashboard')

    def get_form_kwargs(self):
        kwargs = super(VerifyEmailView, self).get_form_kwargs()
        kwargs['user'] = self.get_token_user()
        return kwargs

    def get_token_user(self):
        uid = base36_to_int(self.kwargs['uidb36'])
        return User._default_manager.get(pk=uid)

    def check_token(self):
        user = self.get_token_user()
        token = self.kwargs.get('token')
        if not token or not user:
            return False
        return token_generator.check_token(user, token)

    def get_context_data(self, **kwargs):
        kwargs = super(VerifyEmailView, self).get_context_data(**kwargs)
        kwargs.update({
            'valid_token': self.check_token(),
            'token': self.kwargs.get('token', ''),
        })
        return kwargs

    def form_valid(self, form):
        if not self.check_token():
            return self.form_invalid(form)
        form.user.is_active = True
        user = form.save()
        user = auth.authenticate(
            username=user.email,
            password=form.cleaned_data['new_password1'],
        )
        auth.login(self.request, user)
        messages.success(self.request, 'Your account is now active.')
        return super(VerifyEmailView, self).form_valid(form)

verify_email = VerifyEmailView.as_view()
