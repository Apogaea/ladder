from tests.exchange.utils import (
    assert_is_fulfilled,
    assert_is_active,
    assert_is_reserved,
    assert_not_active_not_reserved_not_fulfilled,
)


def test_request_is_active_with_no_match(factories):
    request = factories.TicketRequestFactory()

    assert_is_active(request)


def test_request_is_active_with_cancelled_match(factories):
    request = factories.TicketRequestFactory()
    factories.TicketMatchFactory(ticket_request=request, is_terminated=True)

    assert_is_active(request)


def test_request_not_active_with_expired_match(factories):
    request = factories.TicketRequestFactory()
    factories.ExpiredTicketMatchFactory(
        ticket_request=request,
    )

    assert_not_active_not_reserved_not_fulfilled(request)


def test_request_not_active_when_terminated(factories):
    request = factories.TicketRequestFactory(is_terminated=True)

    assert_not_active_not_reserved_not_fulfilled(request)


def test_request_not_active_when_cancelled(factories):
    request = factories.TicketRequestFactory(is_cancelled=True)

    assert_not_active_not_reserved_not_fulfilled(request)


def test_is_reserved_with_unaccepted_match(factories):
    request = factories.TicketRequestFactory()
    factories.TicketMatchFactory(ticket_request=request)

    assert_is_reserved(request)


def test_not_reserved_if_offer_cancelled(factories):
    request = factories.TicketRequestFactory()
    offer = factories.TicketOfferFactory(is_cancelled=True)
    factories.TicketMatchFactory(
        ticket_request=request,
        ticket_offer=offer,
    )

    assert_is_active(request)


def test_not_reserved_if_offer_terminated(factories):
    request = factories.TicketRequestFactory()
    offer = factories.TicketOfferFactory(is_cancelled=True)
    factories.TicketMatchFactory(
        ticket_request=request,
        ticket_offer=offer,
    )

    assert_is_active(request)


def test_is_fullfilled(factories):
    request = factories.AcceptedTicketMatchFactory().ticket_request

    assert_is_fulfilled(request)
