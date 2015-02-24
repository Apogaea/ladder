def test_matched_returns_none(factories):
    ticket_request = factories.TicketMatchFactory().ticket_request
    assert ticket_request.place_in_line is None


def test_cancelled_returns_none(factories):
    ticket_request = factories.TicketRequestFactory(is_cancelled=True)
    assert ticket_request.place_in_line is None


def test_terminated_returns_none(factories):
    ticket_request = factories.TicketRequestFactory(is_cancelled=True)
    assert ticket_request.place_in_line is None


def test_front_of_line(factories):
    ticket_request = factories.TicketRequestFactory()
    factories.TicketRequestFactory.create_batch(10)
    assert ticket_request.place_in_line == 0


def test_non_active_requests_are_ignored(factories):
    factories.TicketRequestFactory()  # first place
    factories.TicketRequestFactory(is_terminated=True)
    factories.TicketRequestFactory(is_cancelled=True)
    factories.TicketMatchFactory()
    factories.TicketMatchFactory()
    ticket_request = factories.TicketRequestFactory()
    factories.TicketRequestFactory.create_batch(10)
    assert ticket_request.place_in_line == 1
