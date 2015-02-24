from django.core.urlresolvers import reverse

from rest_framework import status


def test_cancel_offer_page(factories, user_client):
    offer = factories.TicketOfferFactory(user=user_client.user)

    url = reverse('offer-cancel', kwargs={'pk': offer.pk})

    response = user_client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_canceling_an_offer(factories, models, user_client):
    offer = factories.TicketOfferFactory(user=user_client.user)

    url = reverse('offer-cancel', kwargs={'pk': offer.pk})

    response = user_client.post(url)

    expected_location = reverse('dashboard')
    assert response.get('location', '').endswith(expected_location)

    cancelled_offer = models.TicketOffer.objects.get(pk=offer.pk)
    assert cancelled_offer.is_cancelled
