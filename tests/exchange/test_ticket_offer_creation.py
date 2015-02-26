import pytest

from django.core.urlresolvers import reverse
from django.core import mail

from rest_framework import status


def test_offer_creation_for_next_person_in_line(factories, user_webtest_client, models):
    """
    Test creating an offer that gives to the next person in line with a
    recipient waiting.
    """
    user = user_webtest_client.user
    ticket_request = factories.TicketRequestFactory()
    factories.TicketRequestFactory.create_batch(3)

    response = user_webtest_client.get(reverse('offer-create'))
    assert response.status_code == status.HTTP_200_OK

    assert not user.ticket_offers.exists()
    assert not models.TicketMatch.objects.exists()
    assert len(mail.outbox) == 0

    response.forms['auto-match']['ticket_code'] = 'test-code'
    create_response = response.forms['auto-match'].submit('submit')

    assert create_response.status_code == status.HTTP_302_FOUND

    assert user.ticket_offers.exists()
    assert models.TicketMatch.objects.exists()

    updated_ticket_request = models.TicketRequest.objects.get(pk=ticket_request.pk)
    ticket_offer = user.ticket_offers.get()

    assert ticket_offer.is_reserved
    assert ticket_offer.ticket_code == 'test-code'
    assert ticket_request.is_reserved

    assert len(mail.outbox) == 1
    assert ticket_request.user.email in mail.outbox[0].to


@pytest.mark.parametrize(
    'index',
    (1, 2, 3),
)
def test_offer_creation_choosing_recipient(factories, user_webtest_client, models, index):
    """
    Test selecting one of the three choices.
    """
    user = user_webtest_client.user
    factories.TicketRequestFactory.create_batch(4)

    response = user_webtest_client.get(reverse('offer-create'))
    assert response.status_code == status.HTTP_200_OK

    assert not user.ticket_offers.exists()
    assert not models.TicketMatch.objects.exists()
    assert len(mail.outbox) == 0

    form_key = 'recipient-select-{0}'.format(index)
    response.forms[form_key]['ticket_code'] = 'test-code'
    create_response = response.forms[form_key].submit('submit')

    assert create_response.status_code == status.HTTP_302_FOUND

    assert user.ticket_offers.exists()
    assert models.TicketMatch.objects.exists()

    ticket_offer = user.ticket_offers.get()
    assert ticket_offer.ticket_code == 'test-code'

    ticket_match = models.TicketMatch.objects.get()

    ticket_request = models.TicketRequest.objects.order_by('created_at')[index - 1]
    assert ticket_match.ticket_request == ticket_request

    assert len(mail.outbox) == 1
    assert ticket_request.user.email in mail.outbox[0].to


def test_offer_creation_choosing_invalid_non_active_request(factories,
                                                            user_webtest_client,
                                                            models):
    """
    Test that an inactive ticket request cannot be selected.
    """
    user = user_webtest_client.user
    ticket_request = factories.TicketMatchFactory().ticket_request
    factories.TicketRequestFactory.create_batch(3)

    response = user_webtest_client.get(reverse('offer-create'))
    assert response.status_code == status.HTTP_200_OK

    assert not user.ticket_offers.exists()
    assert len(mail.outbox) == 0

    response.forms['recipient-select-1']['ticket_code'] = 'test-code'
    response.forms['recipient-select-1']['ticket_request'].value = ticket_request.pk
    create_response = response.forms['recipient-select-1'].submit('submit')

    assert create_response.status_code == status.HTTP_200_OK

    context_form = create_response.context['form']
    assert 'ticket_request' in context_form.errors

    assert not user.ticket_offers.exists()
    assert len(mail.outbox) == 0


def test_offer_creation_choosing_request_not_in_selection(factories,
                                                          user_webtest_client,
                                                          models):
    """
    Test that a request which is not in the *front* of the line cannot be
    selected.
    """
    user = user_webtest_client.user
    factories.TicketRequestFactory.create_batch(10)
    ticket_request = factories.TicketRequestFactory()

    response = user_webtest_client.get(reverse('offer-create'))
    assert response.status_code == status.HTTP_200_OK

    assert not user.ticket_offers.exists()
    assert len(mail.outbox) == 0

    response.forms['recipient-select-1']['ticket_code'] = 'test-code'
    response.forms['recipient-select-1']['ticket_request'].value = ticket_request.pk
    create_response = response.forms['recipient-select-1'].submit('submit')

    assert create_response.status_code == status.HTTP_200_OK

    context_form = create_response.context['form']
    assert 'ticket_request' in context_form.errors

    updated_ticket_request = models.TicketRequest.objects.get(pk=ticket_request.pk)
    assert ticket_request.is_active

    assert not user.ticket_offers.exists()
    assert len(mail.outbox) == 0
