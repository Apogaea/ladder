from django.core.urlresolvers import reverse

from rest_framework import status


def test_cancel_offer_page(factories, user_client):
    offer = factories.TicketOfferFactory(user=user_client.user)

    url = reverse('offer_cancel', kwargs={'pk': offer.pk})

    response = user_client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_canceling_an_offer(factories, models, user_client):
    offer = factories.TicketOfferFactory(user=user_client.user)

    url = reverse('offer_cancel', kwargs={'pk': offer.pk})

    response = user_client.post(url)

    expected_location = reverse('dashboard')
    assert response.get('location', '').endswith(expected_location)

    cancelled_offer = models.TicketOffer.objects.get(pk=offer.pk)
    assert cancelled_offer.is_cancelled


def test_toggle_automatch_page(factories, models, user_client):
    offer = factories.TicketOfferFactory(user=user_client.user, is_automatch=False)

    url = reverse('offer_toggle_automatch', kwargs={'pk': offer.pk})

    response = user_client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_turning_on_automatch(factories, models, user_client):
    offer = factories.TicketOfferFactory(user=user_client.user, is_automatch=False)

    url = reverse('offer_toggle_automatch', kwargs={'pk': offer.pk})

    response = user_client.post(url)

    expected_location = reverse('offer_detail', kwargs={'pk': offer.pk})
    assert response.get('location', '').endswith(expected_location)

    updated_offer = models.TicketOffer.objects.get(pk=offer.pk)
    assert updated_offer.is_automatch


def test_turning_off_automatch(factories, models, user_client):
    offer = factories.TicketOfferFactory(user=user_client.user, is_automatch=True)

    url = reverse('offer_toggle_automatch', kwargs={'pk': offer.pk})

    response = user_client.post(url)

    expected_location = reverse('offer_select_recipient', kwargs={'pk': offer.pk})
    assert response.get('location', '').endswith(expected_location)

    updated_offer = models.TicketOffer.objects.get(pk=offer.pk)
    assert not updated_offer.is_automatch
