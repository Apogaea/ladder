from ladder.emails import LadderEmail

from emailtools.cbe.mixins import BuildAbsoluteURIMixin


class MatchConfirmationEmail(BuildAbsoluteURIMixin, LadderEmail):
    subject = "[Ladder] Ticket Offer Verification"
    template_name = 'exchange/mail/confirm_offer.html'

    def get_to(self):
        return [self.args[0].ticket_request.user.email]

    def get_context_data(self, **kwargs):
        kwargs = super(MatchConfirmationEmail, self).get_context_data(**kwargs)
        ticket_match = self.args[0]
        kwargs.update({
            'confirm_url': self.reverse_absolute_uri('match_confirm', kwargs={'pk': ticket_match.pk}),
            'ticket_match': ticket_match,
            'ticket_request': ticket_match.ticket_request,
            'ticket_offer': ticket_match.ticket_offer,
        })
        return kwargs

send_match_confirmation_email = MatchConfirmationEmail.as_callable()


class MatchInformationEmail(BuildAbsoluteURIMixin, LadderEmail):
    subject = "[Ladder] Ticket Match Information"

    def get_to(self):
        return [self.args[1].email]

    def get_context_data(self, **kwargs):
        kwargs = super(MatchInformationEmail, self).get_context_data(**kwargs)
        ticket_match = self.args[0]
        kwargs.update({
            'ticket_match': ticket_match,
            'ticket_request': ticket_match.ticket_request,
            'ticket_offer': ticket_match.ticket_offer,
        })
        return kwargs

send_offer_accepted_email = MatchInformationEmail.as_callable(
    template_name='exchange/mail/offer_accepted.html',
)
send_request_fulfilled_email = MatchInformationEmail.as_callable(
    template_name='exchange/mail/request_fulfilled.html',
)
send_offer_rejected_email = MatchInformationEmail.as_callable(
    subject="[Ladder] Ticket Offer Rejected",
    template_name='exchange/mail/offer_rejected.html',
)
