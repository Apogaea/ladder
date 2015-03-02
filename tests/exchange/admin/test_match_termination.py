import pytest

from django.core.urlresolvers import reverse
from django.core import mail

from rest_framework import status


def test_match_termination_page(factories, admin_webtest_client):
    match = factories.TicketMatchFactory()

    terminate_url = reverse('admin:match-terminate', kwargs={'pk': match.pk})

    response = admin_webtest_client.get(terminate_url)

    assert response.status_code == status.HTTP_200_OK


def test_terminating_request_only(factories, admin_webtest_client, models):
    match = factories.TicketMatchFactory()

    terminate_url = reverse('admin:match-terminate', kwargs={'pk': match.pk})

    get_response = admin_webtest_client.get(terminate_url)

    assert get_response.status_code == status.HTTP_200_OK

    response = get_response.forms['terminate-request'].submit()

    assert response.status_code == status.HTTP_302_FOUND

    request = models.TicketRequest.objects.get(pk=match.ticket_request.pk)
    assert request.is_terminated

    offer = models.TicketOffer.objects.get(pk=match.ticket_offer.pk)
    assert not offer.is_terminated


def test_terminating_request_matches_offer_with_next_request(factories, admin_webtest_client, models):
    match = factories.TicketMatchFactory()

    waiting_request = factories.TicketRequestFactory()

    assert not waiting_request.matches.exists()

    terminate_url = reverse('admin:match-terminate', kwargs={'pk': match.pk})

    assert not len(mail.outbox)

    get_response = admin_webtest_client.get(terminate_url)

    assert get_response.status_code == status.HTTP_200_OK

    response = get_response.forms['terminate-request'].submit()

    assert response.status_code == status.HTTP_302_FOUND

    terminated_request = models.TicketRequest.objects.get(pk=match.ticket_request.pk)
    assert terminated_request.is_terminated

    updated_waiting_request = models.TicketRequest.objects.get(pk=waiting_request.pk)
    assert updated_waiting_request.matches.exists()
    assert updated_waiting_request.is_reserved
    new_match = updated_waiting_request.matches.get()
    assert new_match.ticket_offer == match.ticket_offer

    assert len(mail.outbox) == 1


def test_terminating_offer_only(factories, admin_webtest_client, models):
    match = factories.TicketMatchFactory()

    terminate_url = reverse('admin:match-terminate', kwargs={'pk': match.pk})

    get_response = admin_webtest_client.get(terminate_url)

    assert get_response.status_code == status.HTTP_200_OK

    response = get_response.forms['terminate-offer'].submit()

    assert response.status_code == status.HTTP_302_FOUND

    offer = models.TicketOffer.objects.get(pk=match.ticket_offer.pk)
    assert offer.is_terminated

    request = models.TicketRequest.objects.get(pk=match.ticket_request.pk)
    assert not request.is_terminated


def test_terminating_offer_will_auto_match_request_with_active_offer(factories,
                                                                     admin_webtest_client,
                                                                     models):
    match = factories.TicketMatchFactory()

    active_offer = factories.TicketOfferFactory()
    assert not active_offer.matches.exists()

    terminate_url = reverse('admin:match-terminate', kwargs={'pk': match.pk})

    assert not len(mail.outbox)

    get_response = admin_webtest_client.get(terminate_url)

    assert get_response.status_code == status.HTTP_200_OK

    response = get_response.forms['terminate-offer'].submit()

    assert response.status_code == status.HTTP_302_FOUND

    terminated_offer = models.TicketOffer.objects.get(pk=match.ticket_offer.pk)
    assert terminated_offer.is_terminated

    updated_active_offer = models.TicketOffer.objects.get(pk=active_offer.pk)
    assert updated_active_offer.matches.exists()
    assert updated_active_offer.is_reserved
    new_match = updated_active_offer.matches.get()
    assert new_match.ticket_request == match.ticket_request

    assert len(mail.outbox) == 1
