from django.core.management import call_command


def test_match_cleanup_command(factories, models):
    offer = factories.TicketOfferFactory()
    request = factories.TicketRequestFactory()

    assert not models.TicketMatch.objects.exists()

    call_command('handle_expired_matches')

    assert models.TicketMatch.objects.exists()
