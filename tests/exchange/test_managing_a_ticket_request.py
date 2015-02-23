from django.core.urlresolvers import reverse

from rest_framework import status


def test_cancel_request_page(factories, user_client):
    request = factories.TicketRequestFactory(user=user_client.user)

    url = reverse('request_cancel', kwargs={'pk': request.pk})

    response = user_client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_cancelling_request(factories, user_client, models):
    request = factories.TicketRequestFactory(user=user_client.user)

    url = reverse('request_cancel', kwargs={'pk': request.pk})

    response = user_client.post(url)

    expected_location = reverse('dashboard')
    assert response.get('location').endswith(expected_location)
    updated_request = models.TicketRequest.objects.get(pk=request.pk)
    assert updated_request.is_cancelled


def test_match_confirm_page(factories, user_client):
    request = factories.TicketRequestFactory(user=user_client.user)
    match = factories.TicketMatchFactory(ticket_request=request)

    url = reverse('match_confirm', kwargs={'pk': match.pk})

    response = user_client.get(url)

    assert response.status_code == status.HTTP_200_OK
