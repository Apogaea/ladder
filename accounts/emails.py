from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from ladder.emails import LadderEmail


class BuildAbsoluteURIMixin(object):
    protocol = 'https'

    def get_domain(self):
        return Site.objects.get_current().domain

    def get_protocol(self):
        return self.protocol

    def reverse_absolute_uri(self, view_name, args=None, kwargs=None):
        location = reverse(view_name, args=args, kwargs=kwargs)
        return self.build_absolute_uri(location)

    def build_absolute_uri(self, location):
        current_uri = '{protocol}://{domain}{location}'.format(
            protocol=self.get_protocol(),
            domain=self.get_domain(),
            location=location,
        )
        return current_uri


class UserTokenEmailMixin(BuildAbsoluteURIMixin):
    UID_KWARG = 'uidb36'
    TOKEN_KWARG = 'token'

    token_generator = default_token_generator

    def get_user(self):
        return self.args[0]

    def generate_token(self, user):
        return self.token_generator.make_token(user)

    def get_uid(self, user):
        return int_to_base36(user.pk)

    def reverse_token_url(self, view_name, args=None, kwargs={}):
        kwargs.setdefault(self.UID_KWARG, self.get_uid(self.get_user()))
        kwargs.setdefault(self.TOKEN_KWARG, self.generate_token(self.get_user()))
        return self.reverse_absolute_uri(view_name, args=args, kwargs=kwargs)


class RegistrationVerificationEmail(UserTokenEmailMixin, LadderEmail):
    template_name = 'accounts/mail/verify_email.html'
    subject = '[Ladder] Confirm Email Address'

    def get_to(self):
        return [self.get_user().email]

    def get_context_data(self, **kwargs):
        kwargs = super(RegistrationVerificationEmail, self).get_context_data()
        user = self.get_user()
        kwargs.update({
            'user': user,
            'reset_url': self.reverse_token_url('accounts.views.verify_email'),
        })
        return kwargs

send_registration_verification_email = RegistrationVerificationEmail.as_callable()


class PasswordResetEmail(UserTokenEmailMixin, LadderEmail):
    template_name = 'accounts/mail/password_reset.html'
    subject = "[Uadder] Password Reset"

    def get_to(self):
        return [self.get_user().email]

    def get_context_data(self, **kwargs):
        kwargs = super(PasswordResetEmail, self).get_context_data()
        user = self.get_user()
        kwargs.update({
            'user': user,
            'reset_url': self.reverse_token_url('authtools.views.password_reset_confirm_and_login'),
        })
        return kwargs

password_reset_email = PasswordResetEmail.as_callable()
