from tests.exchange.utils import (
    assert_is_fulfilled,
    assert_is_active,
    assert_is_reserved,
    assert_not_active_not_reserved_not_fulfilled,
)


def test_offer_is_active_with_no_match(factories):
    offer = factories.TicketOfferFactory()

    assert_is_active(offer)


def test_offer_is_active_with_cancelled_match(factories):
    offer = factories.TicketOfferFactory()
    factories.TicketMatchFactory(ticket_offer=offer, ticket_request__is_terminated=True)

    assert_is_active(offer)


def test_offer_is_active_with_expired_match(factories):
    offer = factories.TicketOfferFactory()
    factories.ExpiredTicketMatchFactory(
        ticket_offer=offer,
    )

    assert_is_active(offer)


def test_offer_not_active_when_terminated(factories):
    offer = factories.TicketOfferFactory(is_terminated=True)

    assert_not_active_not_reserved_not_fulfilled(offer)


def test_offer_not_active_when_cancelled(factories):
    offer = factories.TicketOfferFactory(is_cancelled=True)

    assert_not_active_not_reserved_not_fulfilled(offer)


def test_is_reserved_with_unaccepted_match(factories):
    offer = factories.TicketOfferFactory()
    factories.TicketMatchFactory(ticket_offer=offer)

    assert_is_reserved(offer)


def test_not_reserved_if_offer_cancelled(factories):
    offer = factories.TicketOfferFactory()
    request = factories.TicketRequestFactory(is_cancelled=True)
    factories.TicketMatchFactory(
        ticket_request=request,
        ticket_offer=offer,
    )

    assert_is_active(offer)


def test_not_reserved_if_offer_terminated(factories):
    offer = factories.TicketOfferFactory()
    request = factories.TicketRequestFactory(is_cancelled=True)
    factories.TicketMatchFactory(
        ticket_request=request,
        ticket_offer=offer,
    )

    assert_is_active(offer)


def test_is_fullfilled(factories):
    offer = factories.AcceptedTicketMatchFactory().ticket_offer

    assert_is_fulfilled(offer)
