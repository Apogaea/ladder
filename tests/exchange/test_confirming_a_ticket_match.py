from django.core.urlresolvers import reverse
from django.core import mail

from rest_framework import status


def test_offer_confirmation(user_client, factories, models):
    ticket_match = factories.TicketMatchFactory(
        ticket_request__user=user_client.user,
    )

    assert len(mail.outbox) == 0

    response = user_client.get(reverse('match-confirm', kwargs={'pk': ticket_match.pk}))
    assert response.status_code == status.HTTP_200_OK

    response = user_client.post(reverse('match-confirm', kwargs={'pk': ticket_match.pk}))
    assert response.status_code == status.HTTP_302_FOUND

    ticket_offer = models.TicketOffer.objects.get(pk=ticket_match.ticket_offer.pk)
    ticket_request = models.TicketRequest.objects.get(pk=ticket_match.ticket_request.pk)
    ticket_match = models.TicketMatch.objects.get(pk=ticket_match.pk)

    assert ticket_offer.is_fulfilled
    assert ticket_request.is_fulfilled
    assert ticket_match.is_accepted

    assert len(mail.outbox) == 2
    to_addresses = [message.to[0] for message in mail.outbox]
    assert ticket_offer.user.email in to_addresses
    assert user_client.user.email in to_addresses
