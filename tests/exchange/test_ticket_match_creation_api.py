import pytest

from django.core import mail


def test_with_no_specified_offer_or_request(factories, models):
    request = factories.TicketRequestFactory()
    offer = factories.TicketOfferFactory()

    match = models.TicketMatch.objects.create_match()

    assert match.ticket_request == request
    assert match.ticket_offer == offer
    assert not mail.outbox


def test_with_specified_ticket_request(factories, models):
    first_request = factories.TicketRequestFactory()
    second_request = factories.TicketRequestFactory()
    offer = factories.TicketOfferFactory()

    match = models.TicketMatch.objects.create_match(ticket_request=second_request)

    assert match.ticket_request == second_request
    assert match.ticket_offer == offer
    assert not mail.outbox


def test_with_specified_ticket_offer(factories, models):
    request = factories.TicketRequestFactory()
    first_offer = factories.TicketOfferFactory()
    second_offer = factories.TicketOfferFactory()

    match = models.TicketMatch.objects.create_match(ticket_offer=second_offer)

    assert match.ticket_request == request
    assert match.ticket_offer == second_offer
    assert not mail.outbox


def test_with_no_active_request(factories, models):
    factories.TicketRequestFactory(is_cancelled=True)
    factories.TicketRequestFactory(is_terminated=True)
    factories.AcceptedTicketMatchFactory()

    factories.TicketOfferFactory()

    with pytest.raises(models.TicketRequest.DoesNotExist):
        models.TicketMatch.objects.create_match()
    assert not mail.outbox


def test_with_no_active_offer(factories, models):
    factories.TicketOfferFactory(is_cancelled=True)
    factories.TicketOfferFactory(is_terminated=True)
    factories.AcceptedTicketMatchFactory()

    factories.TicketRequestFactory()

    with pytest.raises(models.TicketOffer.DoesNotExist):
        models.TicketMatch.objects.create_match()
    assert not mail.outbox


def test_fail_silently(models):
    models.TicketMatch.objects.create_match(fail_silently=True)
    assert not mail.outbox


def test_send_email_option(factories, models):
    request = factories.TicketRequestFactory()
    offer = factories.TicketOfferFactory()

    match = models.TicketMatch.objects.create_match(send_confirmation_email=True)

    assert match.ticket_request == request
    assert match.ticket_offer == offer
    assert len(mail.outbox) == 1
