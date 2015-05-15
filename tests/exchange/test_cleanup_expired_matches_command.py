from django.core.management import call_command


def test_match_cleanup_for_fresh_match_command(factories, models):
    offer = factories.TicketOfferFactory()
    request = factories.TicketRequestFactory()

    assert not models.TicketMatch.objects.exists()

    call_command('handle_expired_matches')

    assert models.TicketMatch.objects.exists()


def test_match_cleanup_for_expired_match_command(factories, models):
    expired_match = factories.ExpiredTicketMatchFactory()
    offer = expired_match.ticket_offer

    pending_request = factories.TicketRequestFactory()

    assert pending_request.is_active
    assert offer.is_active

    call_command('handle_expired_matches')

    assert offer.is_reserved
    assert pending_request.is_reserved
