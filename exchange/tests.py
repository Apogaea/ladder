from __future__ import division
from uuid import uuid4
import datetime
from mock import patch
from contextlib import contextmanager

from django.test import TestCase
from django.utils import timezone
from django.conf import settings

from accounts.models import User
from exchange.models import TicketRequest, TicketOffer, TicketMatch


@contextmanager
def patch_now(when):
    with patch.object(timezone, 'now') as patched_now:
        patched_now.return_value = when
        yield


def user_kwargs():
    return {
        'email': str(uuid4()) + '@example.com',
    }


class TestTicketRequestQueries(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(**user_kwargs())
        self.user2 = User.objects.create(**user_kwargs())

    def test_is_active(self):
        request = TicketRequest.objects.create(user=self.user1)
        offer = TicketOffer.objects.create(user=self.user2)

        self.assertIn(request, TicketRequest.objects.is_active())
        self.assertTrue(request.is_active)
        self.assertNotIn(request, TicketRequest.objects.is_reserved())
        self.assertFalse(request.is_reserved)
        self.assertNotIn(request, TicketRequest.objects.is_fulfilled())
        self.assertFalse(request.is_fulfilled)

        self.assertIn(offer, TicketOffer.objects.is_active())
        self.assertTrue(offer.is_active)
        self.assertNotIn(offer, TicketOffer.objects.is_reserved())
        self.assertFalse(offer.is_reserved)
        self.assertNotIn(offer, TicketOffer.objects.is_fulfilled())
        self.assertFalse(offer.is_fulfilled)

    def test_request_and_offer_cancellation(self):
        request = TicketRequest.objects.create(user=self.user1, is_cancelled=True)
        offer = TicketOffer.objects.create(user=self.user2, is_cancelled=True)

        self.assertIn(request, TicketRequest.objects.is_active())
        self.assertTrue(request.is_active)

        self.assertIn(offer, TicketOffer.objects.is_active())
        self.assertTrue(offer.is_active)

    def test_request_and_offer_termination(self):
        request = TicketRequest.objects.create(user=self.user1, is_terminated=True)
        offer = TicketOffer.objects.create(user=self.user2, is_terminated=True)

        self.assertIn(request, TicketRequest.objects.is_active())
        self.assertTrue(request.is_active)

        self.assertIn(offer, TicketOffer.objects.is_active())
        self.assertTrue(offer.is_active)

    def test_is_reserved(self):
        request = TicketRequest.objects.create(user=self.user1)
        offer = TicketOffer.objects.create(user=self.user2)
        TicketMatch.objects.create(
            ticket_request=request,
            ticket_offer=offer,
        )

        self.assertNotIn(request, TicketRequest.objects.is_active())
        self.assertFalse(request.is_active)
        self.assertIn(request, TicketRequest.objects.is_reserved())
        self.assertTrue(request.is_reserved)
        self.assertNotIn(request, TicketRequest.objects.is_fulfilled())
        self.assertFalse(request.is_fulfilled)

        self.assertNotIn(offer, TicketOffer.objects.is_active())
        self.assertFalse(offer.is_active)
        self.assertIn(offer, TicketOffer.objects.is_reserved())
        self.assertTrue(offer.is_reserved)
        self.assertNotIn(offer, TicketOffer.objects.is_fulfilled())
        self.assertFalse(offer.is_fulfilled)

        with patch_now(timezone.now() + datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME + 1)):
            self.assertIn(request, TicketRequest.objects.is_active())
            self.assertTrue(request.is_active)
            self.assertNotIn(request, TicketRequest.objects.is_reserved())
            self.assertFalse(request.is_reserved)
            self.assertNotIn(request, TicketRequest.objects.is_fulfilled())
            self.assertFalse(request.is_fulfilled)

            self.assertIn(offer, TicketOffer.objects.is_active())
            self.assertTrue(offer.is_active)
            self.assertNotIn(offer, TicketOffer.objects.is_reserved())
            self.assertFalse(offer.is_reserved)
            self.assertNotIn(offer, TicketOffer.objects.is_fulfilled())
            self.assertFalse(offer.is_fulfilled)

    def test_terminated_reservation(self):
        request = TicketRequest.objects.create(user=self.user1)
        offer = TicketOffer.objects.create(user=self.user2)
        TicketMatch.objects.create(
            ticket_request=request,
            ticket_offer=offer,
            is_terminated=True,
        )

        self.assertIn(request, TicketRequest.objects.is_active())
        self.assertTrue(request.is_active)
        self.assertNotIn(offer, TicketOffer.objects.is_reserved())
        self.assertFalse(offer.is_reserved)
        self.assertNotIn(offer, TicketOffer.objects.is_fulfilled())
        self.assertFalse(offer.is_fulfilled)

        self.assertIn(offer, TicketOffer.objects.is_active())
        self.assertTrue(offer.is_active)
        self.assertNotIn(offer, TicketOffer.objects.is_reserved())
        self.assertFalse(offer.is_reserved)
        self.assertNotIn(offer, TicketOffer.objects.is_fulfilled())
        self.assertFalse(offer.is_fulfilled)

    def test_is_fullfilled(self):
        request = TicketRequest.objects.create(user=self.user1)
        offer = TicketOffer.objects.create(user=self.user2)
        TicketMatch.objects.create(
            ticket_request=request,
            ticket_offer=offer,
            accepted_at=timezone.now()
        )

        self.assertNotIn(request, TicketRequest.objects.is_active())
        self.assertFalse(request.is_active)
        self.assertNotIn(request, TicketRequest.objects.is_reserved())
        self.assertFalse(request.is_reserved)
        self.assertIn(request, TicketRequest.objects.is_fulfilled())
        self.assertTrue(request.is_fulfilled)

        self.assertNotIn(offer, TicketOffer.objects.is_active())
        self.assertFalse(offer.is_active)
        self.assertNotIn(offer, TicketOffer.objects.is_reserved())
        self.assertFalse(offer.is_reserved)
        self.assertIn(offer, TicketOffer.objects.is_fulfilled())
        self.assertTrue(offer.is_fulfilled)
