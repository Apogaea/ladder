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
