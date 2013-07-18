from __future__ import division
from uuid import uuid4
import datetime
from mock import patch
from contextlib import contextmanager
import unittest

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse

from accounts.models import User
from exchange.models import (
    TicketRequest, TicketOffer, TicketMatch, LadderProfile, PhoneNumber,
)


@contextmanager
def patch_now(when):
    with patch.object(timezone, 'now') as patched_now:
        patched_now.return_value = when
        yield


def get_user_kwargs():
    return {
        'email': str(uuid4()) + '@example.com',
    }


class TestTicketRequestQueries(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(**get_user_kwargs())
        self.user2 = User.objects.create(**get_user_kwargs())

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

        self.assertNotIn(request, TicketRequest.objects.is_active())
        self.assertFalse(request.is_active)

        self.assertNotIn(offer, TicketOffer.objects.is_active())
        self.assertFalse(offer.is_active)

    def test_request_and_offer_termination(self):
        request = TicketRequest.objects.create(user=self.user1, is_terminated=True)
        offer = TicketOffer.objects.create(user=self.user2, is_terminated=True)

        self.assertNotIn(request, TicketRequest.objects.is_active())
        self.assertFalse(request.is_active)

        self.assertNotIn(offer, TicketOffer.objects.is_active())
        self.assertFalse(offer.is_active)

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
            # Using cached_propertys so we need to refetch them.
            request = TicketRequest.objects.get(pk=request.pk)
            offer = TicketOffer.objects.get(pk=offer.pk)
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


class TestLadderProfileAPI(TestCase):
    def setUp(self):
        self.user = User.objects.create(is_active=True, **get_user_kwargs())
        self.lp = self.user.ladder_profile

    def test_is_verified(self):
        self.assertFalse(self.lp.is_verified)
        self.assertFalse(self.lp.can_offer_ticket)
        self.assertFalse(self.lp.can_request_ticket)
        self.assertNotIn(self.lp, LadderProfile.objects.is_verified())

        self.lp.verified_phone_number = self.lp.phone_numbers.create(**get_phone_number_kwargs(True))
        self.lp.save()
        # LadderProfile.is_verified uses a cached_property
        self.lp = LadderProfile.objects.get(pk=self.lp.pk)

        self.assertTrue(self.lp.is_verified)
        self.assertTrue(self.lp.can_offer_ticket)
        self.assertTrue(self.lp.can_request_ticket)
        self.assertIn(self.lp, LadderProfile.objects.is_verified())

    def test_can_offer(self):
        self.lp.verified_phone_number = self.lp.phone_numbers.create(**get_phone_number_kwargs(True))
        self.lp.save()
        # LadderProfile.is_verified uses a cached_property
        self.lp = LadderProfile.objects.get(pk=self.lp.pk)

        self.assertTrue(self.lp.can_offer_ticket)
        self.assertTrue(self.lp.can_request_ticket)

        self.user.ticket_offers.create()

        # LadderProfile.is_verified uses a cached_property
        self.lp = LadderProfile.objects.get(pk=self.lp.pk)
        self.assertTrue(self.lp.can_offer_ticket)
        self.assertFalse(self.lp.can_request_ticket)

    def test_can_request(self):
        self.lp.verified_phone_number = self.lp.phone_numbers.create(**get_phone_number_kwargs(True))
        self.lp.save()
        # LadderProfile.is_verified uses a cached_property
        self.lp = LadderProfile.objects.get(pk=self.lp.pk)

        self.assertTrue(self.lp.can_offer_ticket)
        self.assertTrue(self.lp.can_request_ticket)

        self.user.ticket_requests.create()

        # LadderProfile.is_verified uses a cached_property
        self.lp = LadderProfile.objects.get(pk=self.lp.pk)
        self.assertFalse(self.lp.can_offer_ticket)
        self.assertFalse(self.lp.can_request_ticket)

    @unittest.expectedFailure
    def test_can_request_with_pending_match(self):
        self.assertFalse(True, 'no test for this yet')

    @unittest.expectedFailure
    def test_can_request_with_fulfilled_match(self):
        self.assertFalse(True, 'no test for this yet')

    @unittest.expectedFailure
    def test_can_request_with_cancelled_request(self):
        self.assertFalse(True, 'no test for this yet')

    @unittest.expectedFailure
    def test_can_request_with_cancelled_offer(self):
        self.assertFalse(True, 'no test for this yet')


def get_phone_number_kwargs(is_verified=False):
    number = hash(str(uuid4())) % 10000000000
    kwargs = {
        'phone_number': number,
    }
    if is_verified:
        kwargs['verified_at'] = timezone.now()
    return kwargs

TWILIO_TEST_SETTINGS = {
    'TWILIO_ACCOUNT_SID': settings.TWILIO_TEST_ACCOUNT_SID,
    'TWILIO_AUTH_TOKEN': settings.TWILIO_TEST_AUTH_TOKEN,
    'TWILIO_PHONE_NUMBER': '+15005550006',
}


@override_settings(**TWILIO_TEST_SETTINGS)
class TestTwilioPhoneInteractions(TestCase):
    TWILIO_VALID_NUMBER = '+15005550006'
    TWILIO_INVALID_NUMBER = '+15005550001'
    TWILIO_CANNOT_SMS_NUMBER = '+15005550002'
    TWILIO_INTERNATIONAL_NUMBER = '+15005550003'
    TWILIO_BLACKLIST_NUMBER = '+15005550004'
    TWILIO_NON_SMS_NUMBER = '+15005550009'

    def setUp(self):
        self.user = User.objects.create(is_active=True, **get_user_kwargs())
        self.lp = self.user.ladder_profile
        self.user.set_password('arstarst')
        self.user.save()
        self.client.login(email=self.user.email, password='arstarst')

    def test_phone_verifiable_api(self):
        phone_number = self.lp.phone_numbers.create(**get_phone_number_kwargs())

        self.assertFalse(phone_number.is_verified)
        self.assertNotIn(phone_number, PhoneNumber.objects.is_verified())

        self.assertTrue(phone_number.is_verifiable)
        self.assertIn(phone_number, PhoneNumber.objects.is_verifiable())

        # Now verify it (remeber cached properties, so refetch the number)
        phone_number.verified_at = timezone.now()
        phone_number.save()
        phone_number = PhoneNumber.objects.get(pk=phone_number.pk)

        self.assertTrue(phone_number.is_verified)
        self.assertIn(phone_number, PhoneNumber.objects.is_verified())

        self.assertFalse(phone_number.is_verifiable)
        self.assertNotIn(phone_number, PhoneNumber.objects.is_verifiable())

    def test_sending_sms(self):
        phone_number = self.lp.phone_numbers.create(phone_number=self.TWILIO_VALID_NUMBER)
        self.assertEqual(phone_number.attempts, 0)
        self.assertTrue(phone_number.can_send)
        phone_number.send_sms()

        self.assertEqual(phone_number.attempts, 1)
        self.assertFalse(phone_number.can_send)

        with patch_now(timezone.now() + datetime.timedelta(seconds=settings.TWILIO_RESEND_MINUTES * 60 + 1)):
            self.assertTrue(phone_number.can_send)

    def test_adding_phone_number_view(self):
        raw_number = '5005550006'
        number = '500-555-0006'
        response = self.client.post(reverse('create_phone_number'), {'phone_number': raw_number})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.lp.phone_numbers.filter(phone_number=number).exists())
        phone_number = self.lp.phone_numbers.get()

        self.assertFalse(phone_number.is_verified)
        self.assertTrue(phone_number.is_verifiable)
        self.assertFalse(phone_number.can_send)

        with patch_now(timezone.now() + datetime.timedelta(seconds=settings.TWILIO_RESEND_MINUTES * 60 + 1)):
            self.assertTrue(phone_number.can_send)

    def test_verify_phone_number_view(self):
        phone_number = self.lp.phone_numbers.create(phone_number='500-555-0006')

        self.assertFalse(phone_number.is_verified)
        self.assertTrue(phone_number.can_send)

        response = self.client.post(
            reverse('verify_phone_number', kwargs={'pk': phone_number.pk}),
            {'code': phone_number.confirmation_code},
        )
        self.assertEqual(response.status_code, 302)
        phone_number = self.lp.phone_numbers.get()

        self.assertTrue(phone_number.is_verified)
        self.assertFalse(phone_number.can_send)

        lp = LadderProfile.objects.get(pk=self.lp.pk)
        self.assertTrue(lp.is_verified)
        self.assertEqual(lp.verified_phone_number_id, phone_number.pk)

    @unittest.expectedFailure
    def test_sms_to_invalid_number(self):
        self.assertFalse(True, 'No test for this')

    @unittest.expectedFailure
    def test_international_number_invalid(self):
        self.assertFalse(True, 'No test for this')

    @unittest.expectedFailure
    def test_adding_duplicate_number(self):
        self.assertFalse(True, 'No test for this')

    @unittest.expectedFailure
    def test_sms_to_non_sms_number(self):
        self.assertFalse(True, 'No test for this')

    @unittest.expectedFailure
    def test_sms_to_blacklist_number(self):
        self.assertFalse(True, 'No test for this')
