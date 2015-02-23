from __future__ import division

from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.tests.factories import UserWithProfileFactory

from exchange.models import (
    TicketMatch,
)
from exchange.tests.factories import (
    TicketRequestFactory, TicketOfferFactory, TicketMatchFactory,
    AcceptedTicketMatchFactory, ExpiredTicketMatchFactory,
)

User = get_user_model()


class MatchableAPITest(object):
    def assert_is_active(self, thing):
        self.assertIn(thing, thing.__class__.objects.is_active())
        self.assertNotIn(thing, thing.__class__.objects.is_reserved())
        self.assertNotIn(thing, thing.__class__.objects.is_fulfilled())

        self.assertTrue(thing.is_active)
        self.assertFalse(thing.is_reserved)
        self.assertFalse(thing.is_fulfilled)

    def assert_is_reserved(self, thing):
        self.assertNotIn(thing, thing.__class__.objects.is_active())
        self.assertIn(thing, thing.__class__.objects.is_reserved())
        self.assertNotIn(thing, thing.__class__.objects.is_fulfilled())

        self.assertFalse(thing.is_active)
        self.assertTrue(thing.is_reserved)
        self.assertFalse(thing.is_fulfilled)

    def assert_is_fulfilled(self, thing):
        self.assertNotIn(thing, thing.__class__.objects.is_active())
        self.assertNotIn(thing, thing.__class__.objects.is_reserved())
        self.assertIn(thing, thing.__class__.objects.is_fulfilled())

        self.assertFalse(thing.is_active)
        self.assertFalse(thing.is_reserved)
        self.assertTrue(thing.is_fulfilled)

    def assert_not_active_not_reserved_not_fulfilled(self, thing):
        self.assertNotIn(thing, thing.__class__.objects.is_active())
        self.assertNotIn(thing, thing.__class__.objects.is_reserved())
        self.assertNotIn(thing, thing.__class__.objects.is_fulfilled())

        self.assertFalse(thing.is_active)
        self.assertFalse(thing.is_reserved)
        self.assertFalse(thing.is_fulfilled)


class TicketRequestAPITest(MatchableAPITest, TestCase):
    def test_request_is_active_with_no_match(self):
        request = TicketRequestFactory()

        self.assert_is_active(request)

    def test_request_is_active_with_cancelled_match(self):
        request = TicketRequestFactory()
        TicketMatchFactory(ticket_request=request, is_terminated=True)

        self.assert_is_active(request)

    def test_request_not_active_with_expired_match(self):
        request = TicketRequestFactory()
        ExpiredTicketMatchFactory(
            ticket_request=request,
        )

        self.assert_not_active_not_reserved_not_fulfilled(request)

    def test_request_not_active_when_terminated(self):
        request = TicketRequestFactory(is_terminated=True)

        self.assert_not_active_not_reserved_not_fulfilled(request)

    def test_request_not_active_when_cancelled(self):
        request = TicketRequestFactory(is_cancelled=True)

        self.assert_not_active_not_reserved_not_fulfilled(request)

    def test_is_reserved_with_unaccepted_match(self):
        request = TicketRequestFactory()
        TicketMatchFactory(ticket_request=request)

        self.assert_is_reserved(request)

    def test_not_reserved_if_offer_cancelled(self):
        request = TicketRequestFactory()
        offer = TicketOfferFactory(is_cancelled=True)
        TicketMatchFactory(
            ticket_request=request,
            ticket_offer=offer,
        )

        self.assert_is_active(request)

    def test_not_reserved_if_offer_terminated(self):
        request = TicketRequestFactory()
        offer = TicketOfferFactory(is_cancelled=True)
        TicketMatchFactory(
            ticket_request=request,
            ticket_offer=offer,
        )

        self.assert_is_active(request)

    def test_is_fullfilled(self):
        request = AcceptedTicketMatchFactory().ticket_request

        self.assert_is_fulfilled(request)


class TicketOfferAPITest(MatchableAPITest, TestCase):
    def test_offer_is_active_with_no_match(self):
        offer = TicketOfferFactory()

        self.assert_is_active(offer)

    def test_offer_is_active_with_cancelled_match(self):
        offer = TicketOfferFactory()
        TicketMatchFactory(ticket_offer=offer, is_terminated=True)

        self.assert_is_active(offer)

    def test_offer_is_active_with_expired_match(self):
        offer = TicketOfferFactory()
        ExpiredTicketMatchFactory(
            ticket_offer=offer,
        )

        self.assert_is_active(offer)

    def test_offer_not_active_when_terminated(self):
        offer = TicketOfferFactory(is_terminated=True)

        self.assert_not_active_not_reserved_not_fulfilled(offer)

    def test_offer_not_active_when_cancelled(self):
        offer = TicketOfferFactory(is_cancelled=True)

        self.assert_not_active_not_reserved_not_fulfilled(offer)

    def test_is_reserved_with_unaccepted_match(self):
        offer = TicketOfferFactory()
        TicketMatchFactory(ticket_offer=offer)

        self.assert_is_reserved(offer)

    def test_not_reserved_if_offer_cancelled(self):
        offer = TicketOfferFactory()
        request = TicketRequestFactory(is_cancelled=True)
        TicketMatchFactory(
            ticket_request=request,
            ticket_offer=offer,
        )

        self.assert_is_active(offer)

    def test_not_reserved_if_offer_terminated(self):
        offer = TicketOfferFactory()
        request = TicketRequestFactory(is_cancelled=True)
        TicketMatchFactory(
            ticket_request=request,
            ticket_offer=offer,
        )

        self.assert_is_active(offer)

    def test_is_fullfilled(self):
        offer = AcceptedTicketMatchFactory().ticket_offer

        self.assert_is_fulfilled(offer)


class TicketMatchAPITest(TestCase):
    def test_is_awaiting_confirmation(self):
        match = TicketMatchFactory()

        self.assertTrue(match.is_awaiting_confirmation)
        self.assertIn(match, TicketMatch.objects.is_awaiting_confirmation())

    def test_is_accepted(self):
        match = AcceptedTicketMatchFactory()
        self.assertTrue(match.is_accepted)
        self.assertIn(match, TicketMatch.objects.is_accepted())

    def test_is_expired(self):
        match = ExpiredTicketMatchFactory()

        self.assertTrue(match.is_expired)
        self.assertIn(match, TicketMatch.objects.is_expired())


class LadderProfileAPITest(TestCase):
    def setUp(self):
        self.user = UserWithProfileFactory()

    def test_can_offer_with_no_requests_or_offers(self):
        self.assertTrue(self.user.profile.can_offer_ticket)

    def test_can_request_with_no_requests_or_offers(self):
        self.assertTrue(self.user.profile.can_request_ticket)

    def test_cannot_request_with_active_request(self):
        TicketRequestFactory(user=self.user)
        self.assertFalse(self.user.profile.can_request_ticket)

    def test_exchange_permissions_with_pending_match(self):
        ticket_request = TicketRequestFactory(user=self.user)
        ticket_offer = TicketOfferFactory()
        TicketMatchFactory(
            ticket_request=ticket_request,
            ticket_offer=ticket_offer,
        )

        self.assertFalse(self.user.profile.can_offer_ticket)
        self.assertFalse(self.user.profile.can_request_ticket)

        self.assertTrue(ticket_offer.user.profile.can_offer_ticket)
        self.assertFalse(ticket_offer.user.profile.can_request_ticket)

    def test_can_request_with_fulfilled_match(self):
        ticket_request = TicketRequestFactory(user=self.user)
        ticket_offer = TicketOfferFactory()
        AcceptedTicketMatchFactory(
            ticket_request=ticket_request,
            ticket_offer=ticket_offer,
        )

        self.assertTrue(self.user.profile.can_offer_ticket)
        self.assertTrue(self.user.profile.can_request_ticket)

        self.assertTrue(ticket_offer.user.profile.can_offer_ticket)
        self.assertTrue(ticket_offer.user.profile.can_request_ticket)

    def test_can_request_with_cancelled_request(self):
        TicketRequestFactory(user=self.user, is_cancelled=True)

        self.assertTrue(self.user.profile.can_offer_ticket)
        self.assertTrue(self.user.profile.can_request_ticket)

    def test_can_request_with_expired_match(self):
        request = TicketRequestFactory(user=self.user)
        ExpiredTicketMatchFactory(ticket_request=request)

        self.assertTrue(self.user.profile.can_offer_ticket)
        self.assertTrue(self.user.profile.can_request_ticket)
