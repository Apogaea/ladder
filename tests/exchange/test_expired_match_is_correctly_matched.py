from django.core.urlresolvers import reverse
from django.core import mail

from rest_framework import status


def test_expired_match_offer_is_correctly_matched(factories, user_client, models):
    """
    Test the situation where a match expires, leaving the ticket offer
    up-for-grabs.  This offer should be matched with the next person in line as
    opposed to the next person who requests a ticket.
    """
    # this request *should* be matched next
    pending_request = factories.TicketRequestFactory()
    assert not pending_request.matches.exists()

    match = factories.ExpiredTicketMatchFactory()

    # sanity checks
    assert match.is_expired
    assert match in models.TicketMatch.objects.is_expired()

    request = match.ticket_request
    assert not request.is_active
    assert request not in models.TicketRequest.objects.is_active()

    offer = match.ticket_offer
    assert offer.is_active
    assert offer in models.TicketOffer.objects.is_active()

    # Now create a new request
    create_request_url = reverse('request-create')

    user = user_client.user
    assert not user.ticket_requests.exists()

    response = user_client.post(create_request_url, {
        'message': 'A request message',
    })
    assert response.status_code == status.HTTP_302_FOUND

    # This new request should not be matched with an offer.
    created_request = user.ticket_requests.get()
    assert created_request.is_active

    # The pending request should have been consumed.
    assert offer.is_reserved
    assert pending_request.is_reserved

    assert len(mail.outbox) == 1
