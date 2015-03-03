import urllib

from emailtools import mixins

from ladder.apps.accounts.utils import reverse_registration_url

from ladder.core.emails import LadderEmail


class RegistrationVerificationEmail(mixins.BuildAbsoluteURIMixin, LadderEmail):
    template_name = 'accounts/mail/verify_email.html'
    subject = 'Welcome to the Apogaea Ticket Exchange'

    def __init__(self, email, phone_number, pre_registration_token=None):
        self.to = email
        self.phone_number = phone_number
        self.pre_registration_token = pre_registration_token

    def get_context_data(self, **kwargs):
        kwargs = super(RegistrationVerificationEmail, self).get_context_data(**kwargs)
        confirm_email_url = self.build_absolute_uri(
            reverse_registration_url(self.to, self.phone_number),
        )
        if self.pre_registration_token:
            confirm_email_url = '?'.join((
                confirm_email_url,
                urllib.urlencode({'token': self.pre_registration_token}),
            ))
        kwargs['confirm_email_url'] = confirm_email_url
        return kwargs

send_registration_verification_email = RegistrationVerificationEmail.as_callable()
