from django.utils import timezone


def test_request_creation_history_event(factories, models):
    assert not models.TicketRequestHistory.objects.exists()

    request = factories.TicketRequestFactory()

    assert request.history.count() == 1

    # double check we don't get a second event on another save.
    request.save()
    assert request.history.count() == 1


def test_request_cancellation_history_event(factories, models):
    request = factories.TicketRequestFactory()

    num_entries = request.history.count()

    request.is_cancelled = True
    request.save()

    assert request.history.count() == num_entries + 1


def test_request_termination_history_event(factories, models):
    request = factories.TicketRequestFactory()

    num_entries = request.history.count()

    request.is_terminated = True
    request.save()

    assert request.history.count() == num_entries + 1


def test_request_undo_termination_history_event(factories, models):
    request = factories.TicketRequestFactory(is_terminated=True)

    num_entries = request.history.count()

    request.is_terminated = False
    request.save()

    assert request.history.count() == num_entries + 1


def test_request_match_creation_history_event(factories, models):
    request = factories.TicketRequestFactory()

    num_entries = request.history.count()

    factories.TicketMatchFactory(ticket_request=request)

    assert request.history.count() == num_entries + 1


def test_request_match_confirmation_history_event(factories, models):
    request = factories.TicketRequestFactory()
    match = factories.TicketMatchFactory(ticket_request=request)

    num_entries = request.history.count()

    match.accepted_at = timezone.now()
    match.save()

    assert request.history.count() == num_entries + 1


def test_request_match_termination_history_event(factories, models):
    request = factories.TicketRequestFactory()
    match = factories.TicketMatchFactory(ticket_request=request)

    num_entries = request.history.count()

    match.is_terminated = True
    match.save()

    assert request.history.count() == num_entries + 1


def test_request_match_undo_termination_history_event(factories, models):
    request = factories.TicketRequestFactory()
    match = factories.TicketMatchFactory(ticket_request=request, is_terminated=True)

    num_entries = request.history.count()

    match.is_terminated = False
    match.save()

    assert request.history.count() == num_entries + 1
