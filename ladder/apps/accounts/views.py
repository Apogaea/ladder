import logging

from django.views.generic import FormView, TemplateView, UpdateView, CreateView
from django.core import signing
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from django.core.urlresolvers import reverse, reverse_lazy

from betterforms.forms import BetterForm

from authtools.views import LoginRequiredMixin

from ladder.apps.exchange.models import LadderProfile

from ladder.apps.accounts.forms import UserChangeForm, InitiateRegistrationForm, UserCreationForm
from ladder.apps.accounts.utils import (
    unsign_registration_token, send_phone_number_verification_sms,
)
from ladder.apps.accounts.models import User
from ladder.apps.accounts.emails import send_registration_verification_email

logger = logging.getLogger(__name__)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'


class EditAccountView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/account_edit.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user

    def get_initial(self):
        initial = super(EditAccountView, self).get_initial()
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Your profile was successfully updated")
        return super(EditAccountView, self).form_valid(form)


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = InitiateRegistrationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        send_registration_verification_email(email, phone_number)
        logger.info("REGISTRATION INITIATED: %s - %s", email, phone_number)
        return super(RegisterView, self).form_valid(form)


class RegisterSuccessView(TemplateView):
    template_name = 'accounts/register_success.html'


class VerifyTokenMixin(object):
    def dispatch(self, *args, **kwargs):
        # Ensure token is valid.
        try:
            self.email, self.phone_number = unsign_registration_token(
                self.kwargs['token'],
            )
        except signing.BadSignature:
            return self.render_to_response({})
        # Ensure user does not already exist.
        try:
            User.objects.get(email__iexact=self.email)
            return self.render_to_response({'email_already_registered': True})
        except User.DoesNotExist:
            pass
        # Ensure phone_number is not taken.
        try:
            User.objects.get(_profile__phone_number=self.phone_number)
            return self.render_to_response({'phone_number_already_registered': True})
        except User.DoesNotExist:
            pass
        return super(VerifyTokenMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(VerifyTokenMixin, self).get_context_data(**kwargs)
        kwargs.update({
            'token_valid': True,
            'token': self.kwargs['token'],
            'email': self.email,
            'phone_number': self.phone_number,
        })
        return kwargs


class RegisterConfirmView(VerifyTokenMixin, FormView):
    form_class = BetterForm
    template_name = 'accounts/register_confirm.html'

    def get_success_url(self, **kwargs):
        return reverse('register-verify-phone-number', kwargs=self.kwargs)

    def form_valid(self, form):
        send_phone_number_verification_sms(self.phone_number)
        return super(RegisterConfirmView, self).form_valid(form)


class RegisterVerifyPhoneNumberView(VerifyTokenMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/register_verify_phone_number.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super(RegisterVerifyPhoneNumberView, self).get_form_kwargs()
        kwargs['phone_number'] = self.phone_number
        return kwargs

    def form_valid(self, form):
        # TODO: sms code verification
        form.instance.email = self.email
        form.instance.is_active = True
        self.object = user = form.save()

        LadderProfile.objects.create(
            user=user,
            phone_number=self.phone_number,
        )

        user = authenticate(
            username=user.email,
            password=form.cleaned_data['password'],
        )
        if not user:
            form.add_error(None, 'An error has occured.')
            return self.form_invalid(form)

        auth_login(self.request, user)

        logger.info("REGISTRATION COMPLETED: user:%s".format(user.pk))

        return redirect(self.success_url)
