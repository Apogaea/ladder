def test_is_awaiting_confirmation(factories, models):
    match = factories.TicketMatchFactory()

    assert match.is_awaiting_confirmation
    assert match in models.TicketMatch.objects.is_awaiting_confirmation()


def test_is_accepted(factories, models):
    match = factories.AcceptedTicketMatchFactory()
    assert match.is_accepted
    assert match in models.TicketMatch.objects.is_accepted()


def test_is_expired(factories, models):
    match = factories.ExpiredTicketMatchFactory()

    assert match.is_expired
    assert match in models.TicketMatch.objects.is_expired()


#
# is_terminated
#
def test_is_not_terminated(factories, models):
    match = factories.ExpiredTicketMatchFactory()

    assert not match.is_terminated

def test_is_terminated_via_request(factories, models):
    match = factories.ExpiredTicketMatchFactory(ticket_request__is_terminated=True)

    assert match.is_terminated
    assert match in models.TicketMatch.objects.is_terminated()


def test_is_terminated_via_offer(factories, models):
    match = factories.ExpiredTicketMatchFactory(ticket_offer__is_terminated=True)

    assert match.is_terminated
    assert match in models.TicketMatch.objects.is_terminated()


def test_is_terminated_via_both_offer_and_request(factories, models):
    match = factories.ExpiredTicketMatchFactory(
        ticket_request__is_terminated=True,
        ticket_offer__is_terminated=True,
    )

    assert match.is_terminated
    assert match in models.TicketMatch.objects.is_terminated()


#
# is_cancelled
#
def test_is_not_cancelled(factories, models):
    match = factories.ExpiredTicketMatchFactory()

    assert not match.is_cancelled

def test_is_cancelled_via_request(factories, models):
    match = factories.ExpiredTicketMatchFactory(ticket_request__is_cancelled=True)

    assert match.is_cancelled
    assert match in models.TicketMatch.objects.is_cancelled()


def test_is_cancelled_via_offer(factories, models):
    match = factories.ExpiredTicketMatchFactory(ticket_offer__is_cancelled=True)

    assert match.is_cancelled
    assert match in models.TicketMatch.objects.is_cancelled()


def test_is_cancelled_via_both_offer_and_request(factories, models):
    match = factories.ExpiredTicketMatchFactory(
        ticket_request__is_cancelled=True,
        ticket_offer__is_cancelled=True,
    )

    assert match.is_cancelled
    assert match in models.TicketMatch.objects.is_cancelled()
