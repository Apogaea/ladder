from django.core.urlresolvers import reverse
from django.core import mail

from rest_framework import status


def test_automatic_offer_creation_view(factories, user_client, models):
    ticket_request = factories.TicketRequestFactory()

    response = user_client.get(reverse('offer_create'))

    assert response.status_code == status.HTTP_200_OK

    assert not user_client.user.ticket_offers.exists()
    assert not models.TicketMatch.objects.exists()
    assert len(mail.outbox) == 0

    response = user_client.post(reverse('offer_create'), {'is_automatch': True})
    assert response.status_code == status.HTTP_302_FOUND

    assert user_client.user.ticket_offers.exists()
    assert models.TicketMatch.objects.exists()

    assert len(mail.outbox) == 1
    assert ticket_request.user.email in mail.outbox[0].to


def test_manual_offer_creation_doesnt_auto_match(factories, user_client, models):
    ticket_request = factories.TicketRequestFactory()

    response = user_client.get(reverse('offer_create'))
    assert response.status_code == status.HTTP_200_OK

    assert not user_client.user.ticket_offers.exists()
    assert not models.TicketMatch.objects.exists()
    assert len(mail.outbox) == 0

    response = user_client.post(reverse('offer_create'), {'is_automatch': False})
    assert response.status_code == status.HTTP_302_FOUND

    assert user_client.user.ticket_offers.exists()
    assert not models.TicketMatch.objects.exists()

    ticket_offer = user_client.user.ticket_offers.get()

    assert ticket_offer.is_active
    assert ticket_request.is_active

    assert len(mail.outbox) == 0
