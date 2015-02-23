from emailtools import mixins

from ladder.apps.accounts.utils import reverse_registration_url

from ladder.core.emails import LadderEmail


class RegistrationVerificationEmail(mixins.BuildAbsoluteURIMixin, LadderEmail):
    template_name = 'accounts/mail/verify_email.html'
    subject = 'Welcome to the Apogaea Ticket Exchange'

    def __init__(self, email, phone_number):
        self.to = email
        self.phone_number = phone_number

    def get_context_data(self, **kwargs):
        kwargs = super(RegistrationVerificationEmail, self).get_context_data(**kwargs)
        kwargs.update({
            'confirm_email_url': self.build_absolute_uri(
                reverse_registration_url(self.to, self.phone_number),
            ),
        })
        return kwargs

send_registration_verification_email = RegistrationVerificationEmail.as_callable()
