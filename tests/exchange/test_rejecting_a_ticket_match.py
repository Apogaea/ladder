from django.core.urlresolvers import reverse
from django.core import mail

from rest_framework import status


def test_offer_rejection(factories, user_client, models):
    ticket_match = factories.TicketMatchFactory(
        ticket_request__user=user_client.user,
    )

    assert len(mail.outbox) == 0

    response = user_client.get(reverse('match_confirm', kwargs={'pk': ticket_match.pk}))
    assert response.status_code == status.HTTP_200_OK

    response = user_client.post(
        reverse('match_confirm', kwargs={'pk': ticket_match.pk}),
        {'_reject': True},
    )
    assert response.status_code == status.HTTP_302_FOUND

    ticket_offer = models.TicketOffer.objects.get(pk=ticket_match.ticket_offer.pk)
    ticket_request = models.TicketRequest.objects.get(pk=ticket_match.ticket_request.pk)
    ticket_match = models.TicketMatch.objects.get(pk=ticket_match.pk)

    assert ticket_offer.is_active
    assert ticket_request.is_cancelled
    assert ticket_match.is_terminated

    assert len(mail.outbox) == 0


def test_offer_rejection_is_automatched(user_client, factories, models):
    ticket_match = factories.TicketMatchFactory(
        ticket_request__user=user_client.user,
    )

    pending_request = factories.TicketRequestFactory()

    assert len(mail.outbox) == 0

    response = user_client.post(
        reverse('match_confirm', kwargs={'pk': ticket_match.pk}),
        {'_reject': True},
    )
    assert response.status_code == status.HTTP_302_FOUND

    ticket_offer = models.TicketOffer.objects.get(pk=ticket_match.ticket_offer.pk)
    ticket_request = models.TicketRequest.objects.get(pk=ticket_match.ticket_request.pk)
    ticket_match = models.TicketMatch.objects.get(pk=ticket_match.pk)

    assert ticket_offer.is_reserved
    assert pending_request.is_reserved
    assert ticket_request.is_cancelled
    assert ticket_match.is_terminated

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to, pending_request.user.email
