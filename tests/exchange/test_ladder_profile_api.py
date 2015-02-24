def test_can_offer_with_no_requests_or_offers(user):
    assert user.profile.can_offer_ticket


def test_can_request_with_no_requests_or_offers(user):
    assert user.profile.can_request_ticket


def test_cannot_request_with_active_request(user, factories):
    factories.TicketRequestFactory(user=user)
    assert not user.profile.can_request_ticket


def test_exchange_permissions_with_pending_match(user, factories):
    ticket_request = factories.TicketRequestFactory(user=user)
    ticket_offer = factories.TicketOfferFactory()
    factories.TicketMatchFactory(
        ticket_request=ticket_request,
        ticket_offer=ticket_offer,
    )

    assert not user.profile.can_offer_ticket
    assert not user.profile.can_request_ticket

    assert ticket_offer.user.profile.can_offer_ticket
    assert not ticket_offer.user.profile.can_request_ticket


def test_can_request_with_fulfilled_match(user, factories):
    ticket_request = factories.TicketRequestFactory(user=user)
    ticket_offer = factories.TicketOfferFactory()
    factories.AcceptedTicketMatchFactory(
        ticket_request=ticket_request,
        ticket_offer=ticket_offer,
    )

    assert user.profile.can_offer_ticket
    assert user.profile.can_request_ticket

    assert ticket_offer.user.profile.can_offer_ticket
    assert ticket_offer.user.profile.can_request_ticket


def test_can_request_with_cancelled_request(user, factories):
    factories.TicketRequestFactory(user=user, is_cancelled=True)

    assert user.profile.can_offer_ticket
    assert user.profile.can_request_ticket


def test_can_request_with_expired_match(user, factories):
    request = factories.TicketRequestFactory(user=user)
    factories.ExpiredTicketMatchFactory(ticket_request=request)

    assert user.profile.can_offer_ticket
    assert user.profile.can_request_ticket
