from django.utils import timezone


def test_offer_creation_history_event(factories, models):
    assert not models.TicketOffer.objects.exists()

    offer = factories.TicketOfferFactory()

    assert offer.history.count() == 1

    # double check we don't get a second event on another save.
    offer.save()
    assert offer.history.count() == 1


def test_offer_cancellation_history_event(factories, models):
    offer = factories.TicketOfferFactory()

    num_entries = offer.history.count()

    offer.is_cancelled = True
    offer.save()

    assert offer.history.count() == num_entries + 1


def test_offer_termination_history_event(factories, models):
    offer = factories.TicketOfferFactory()

    num_entries = offer.history.count()

    offer.is_terminated = True
    offer.save()

    assert offer.history.count() == num_entries + 1


def test_offer_undo_termination_history_event(factories, models):
    offer = factories.TicketOfferFactory(is_terminated=True)

    num_entries = offer.history.count()

    offer.is_terminated = False
    offer.save()

    assert offer.history.count() == num_entries + 1


def test_offer_match_creation_history_event(factories, models):
    offer = factories.TicketOfferFactory()

    num_entries = offer.history.count()

    factories.TicketMatchFactory(ticket_offer=offer)

    assert offer.history.count() == num_entries + 1


def test_offer_match_confirmation_history_event(factories, models):
    offer = factories.TicketOfferFactory()
    match = factories.TicketMatchFactory(ticket_offer=offer)

    num_entries = offer.history.count()

    match.accepted_at = timezone.now()
    match.save()

    assert offer.history.count() == num_entries + 1
