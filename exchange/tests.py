from __future__ import division
from uuid import uuid4
import datetime
from mock import patch
from contextlib import contextmanager
import unittest

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
from django.core import mail
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

    def test_not_reserved_when_other_party_cancels(self):
        request = TicketRequest.objects.create(user=self.user1)
        offer = TicketOffer.objects.create(user=self.user2)
        TicketMatch.objects.create(
            ticket_request=request,
            ticket_offer=offer,
        )
        request.is_cancelled = True
        request.save()

        self.assertFalse(offer.is_reserved)
        self.assertNotIn(offer, TicketOffer.objects.is_reserved())
        self.assertTrue(offer.is_active)
        self.assertIn(offer, TicketOffer.objects.is_active())

        request.is_cancelled = False
        request.save()
        offer.is_cancelled = True
        offer.save()

        self.assertFalse(request.is_reserved)
        self.assertNotIn(request, TicketRequest.objects.is_reserved())
        self.assertTrue(request.is_active)
        self.assertIn(request, TicketRequest.objects.is_active())

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


class TestTicketMatchQueryAPI(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(**get_user_kwargs())
        self.user2 = User.objects.create(**get_user_kwargs())
        self.ticket_request = TicketRequest.objects.create(user=self.user1)
        self.ticket_offer = TicketOffer.objects.create(user=self.user2)

    def test_is_awaiting_confirmation(self):
        match = TicketMatch.objects.create(
            ticket_request=self.ticket_request,
            ticket_offer=self.ticket_offer,
        )
        self.assertTrue(match.is_awaiting_confirmation)
        self.assertIn(match, TicketMatch.objects.is_awaiting_confirmation())

    def test_is_accepted(self):
        match = TicketMatch.objects.create(
            ticket_request=self.ticket_request,
            ticket_offer=self.ticket_offer,
            accepted_at=timezone.now(),
        )
        self.assertTrue(match.is_accepted)
        self.assertIn(match, TicketMatch.objects.is_accepted())

    def test_is_expired(self):
        match = TicketMatch.objects.create(
            ticket_request=self.ticket_request,
            ticket_offer=self.ticket_offer,
        )
        with patch_now(timezone.now() + datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME + 1)):
            self.assertTrue(match.is_expired)
            self.assertIn(match, TicketMatch.objects.is_expired())


class TestLadderProfileAPI(TestCase):
    def setUp(self):
        self.user = User.objects.create(is_active=True, **get_user_kwargs())
        self.lp = self.user.ladder_profile
        self.other_user = User.objects.create(is_active=True, **get_user_kwargs())
        self.other_lp = self.other_user.ladder_profile

    def verify_users(self):
        self.lp.verified_phone_number = self.lp.phone_numbers.create(**get_phone_number_kwargs(True))
        self.lp.save()
        self.other_lp.verified_phone_number = self.other_lp.phone_numbers.create(**get_phone_number_kwargs(True))
        self.other_lp.save()
        self.refresh_users()

    def refresh_users(self):
        self.lp = LadderProfile.objects.get(pk=self.lp.pk)
        self.other_lp = LadderProfile.objects.get(pk=self.other_lp.pk)

    def test_is_verified(self):
        self.assertFalse(self.lp.is_verified)
        self.assertFalse(self.lp.can_offer_ticket)
        self.assertFalse(self.lp.can_request_ticket)
        self.assertNotIn(self.lp, LadderProfile.objects.is_verified())

        self.verify_users()

        self.assertTrue(self.lp.is_verified)
        self.assertTrue(self.lp.can_offer_ticket)
        self.assertTrue(self.lp.can_request_ticket)
        self.assertIn(self.lp, LadderProfile.objects.is_verified())

    def test_can_offer(self):
        self.verify_users()

        self.user.ticket_requests.create()
        self.other_user.ticket_offers.create()

        self.refresh_users()

        self.assertFalse(self.lp.can_offer_ticket)
        self.assertTrue(self.other_lp.can_offer_ticket)

    def test_can_request(self):
        self.verify_users()

        self.user.ticket_requests.create()
        self.other_user.ticket_offers.create()

        self.refresh_users()

        self.assertFalse(self.lp.can_request_ticket)
        self.assertFalse(self.other_lp.can_request_ticket)

    def test_exchange_permissions_with_pending_match(self):
        self.verify_users()

        ticket_request = self.user.ticket_requests.create()
        ticket_offer = self.other_user.ticket_offers.create()
        TicketMatch.objects.create(
            ticket_request=ticket_request,
            ticket_offer=ticket_offer,
        )

        self.refresh_users()

        self.assertFalse(self.lp.can_offer_ticket)
        self.assertFalse(self.lp.can_request_ticket)

        self.assertTrue(self.other_lp.can_offer_ticket)
        self.assertFalse(self.other_lp.can_request_ticket)

    def test_can_request_with_fulfilled_match(self):
        self.verify_users()

        ticket_request = self.user.ticket_requests.create()
        ticket_offer = self.other_user.ticket_offers.create()
        TicketMatch.objects.create(
            ticket_request=ticket_request,
            ticket_offer=ticket_offer,
            accepted_at=timezone.now(),
        )

        self.refresh_users()

        self.assertTrue(self.lp.can_offer_ticket)
        self.assertTrue(self.lp.can_request_ticket)

        self.assertTrue(self.other_lp.can_offer_ticket)
        self.assertTrue(self.other_lp.can_request_ticket)

    def test_can_request_with_cancelled_request(self):
        self.verify_users()

        ticket_request = self.user.ticket_requests.create()
        ticket_offer = self.other_user.ticket_offers.create()
        TicketMatch.objects.create(
            ticket_request=ticket_request,
            ticket_offer=ticket_offer,
        )
        ticket_request.is_cancelled = True
        ticket_request.save()

        self.refresh_users()

        self.assertTrue(self.lp.can_offer_ticket)
        self.assertTrue(self.lp.can_request_ticket)

        self.assertTrue(self.other_lp.can_offer_ticket)
        self.assertFalse(self.other_lp.can_request_ticket)

    def test_can_request_with_cancelled_offer(self):
        self.verify_users()

        ticket_offer = self.user.ticket_offers.create()

        self.assertFalse(self.lp.can_request_ticket)

        ticket_offer.is_cancelled = True
        ticket_offer.save()

        self.refresh_users()
        self.assertTrue(self.lp.can_request_ticket)


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
class TestPhoneNumberInteractions(TestCase):
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
        self.assertTrue(phone_number.can_send)
        phone_number.send_sms()

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

    def test_adding_duplicate_number(self):
        self.lp.phone_numbers.create(phone_number='500-555-0006')
        self.assertEqual(self.lp.phone_numbers.count(), 1)

        # unformatted
        response = self.client.post(reverse('create_phone_number'), {'phone_number': '5005550006'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.lp.phone_numbers.count(), 1)

        # formatted
        response = self.client.post(reverse('create_phone_number'), {'phone_number': '500-555-0006'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.lp.phone_numbers.count(), 1)

    def test_adding_someone_elses_number(self):
        other_user = User.objects.create(is_active=True, **get_user_kwargs())
        other_user.ladder_profile.phone_numbers.create(phone_number='500-555-0006', verified_at=timezone.now())

        # unformatted
        response = self.client.post(reverse('create_phone_number'), {'phone_number': '5005550006'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.lp.phone_numbers.exists())

        # formatted
        response = self.client.post(reverse('create_phone_number'), {'phone_number': '500-555-0006'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.lp.phone_numbers.exists())

    @unittest.expectedFailure
    def test_sms_to_invalid_number(self):
        self.assertFalse(True, 'No test for this')

    @unittest.expectedFailure
    def test_international_number_invalid(self):
        self.assertFalse(True, 'No test for this')

    @unittest.expectedFailure
    def test_sms_to_non_sms_number(self):
        self.assertFalse(True, 'No test for this')

    @unittest.expectedFailure
    def test_sms_to_blacklist_number(self):
        self.assertFalse(True, 'No test for this')


class TestExchangeRequestAndOfferViews(TestCase):
    def setUp(self):
        self.user = User.objects.create(is_active=True, **get_user_kwargs())
        self.lp = self.user.ladder_profile
        self.lp.verified_phone_number = self.lp.phone_numbers.create(phone_number='500-555-0006', verified_at=timezone.now())
        self.lp.save()
        self.user.set_password('arstarst')
        self.user.save()
        self.client.login(email=self.user.email, password='arstarst')

        self.other_user = User.objects.create(is_active=True, **get_user_kwargs())
        self.other_lp = self.other_user.ladder_profile
        self.other_lp.save()
        self.other_lp.verified_phone_number = self.other_lp.phone_numbers.create(phone_number='500-555-0006', verified_at=timezone.now())

    def test_automatic_offer_creation_view(self):
        ticket_request = self.other_user.ticket_requests.create()

        response = self.client.get(reverse('offer_create'))
        self.assertEqual(response.status_code, 200)

        self.assertFalse(self.user.ticket_offers.exists())
        self.assertFalse(TicketMatch.objects.exists())
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(reverse('offer_create'), {'is_automatch': True})
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.user.ticket_offers.exists())
        self.assertTrue(TicketMatch.objects.exists())

        ticket_offer = self.user.ticket_offers.get()

        self.assertTrue(ticket_offer.is_reserved)
        self.assertTrue(ticket_request.is_reserved)

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[0].to, self.other_user.email)

    def test_manual_offer_creation_doesnt_match(self):
        ticket_request = self.other_user.ticket_requests.create()

        response = self.client.get(reverse('offer_create'))
        self.assertEqual(response.status_code, 200)

        self.assertFalse(self.user.ticket_offers.exists())
        self.assertFalse(TicketMatch.objects.exists())
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(reverse('offer_create'), {'is_automatch': False})
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.user.ticket_offers.exists())
        self.assertFalse(TicketMatch.objects.exists())

        ticket_offer = self.user.ticket_offers.get()

        self.assertTrue(ticket_offer.is_active)
        self.assertTrue(ticket_request.is_active)

        self.assertEqual(len(mail.outbox), 0)

    def test_request_creation_view(self):
        response = self.client.get(reverse('request_create'))
        self.assertEqual(response.status_code, 200)

        self.assertFalse(self.user.ticket_requests.exists())

        response = self.client.post(reverse('request_create'), {'message': 'A nice heartfelt message'})
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.user.ticket_requests.exists())

        ticket_request = self.user.ticket_requests.get()

        self.assertTrue(ticket_request.is_active)

    def test_automatic_request_matching(self):
        ticket_offer = self.other_user.ticket_offers.create(is_automatch=True)

        self.assertFalse(self.user.ticket_requests.exists())
        self.assertFalse(TicketMatch.objects.exists())

        response = self.client.post(reverse('request_create'), {'message': 'A nice heartfelt message'})
        self.assertEqual(response.status_code, 302)

        ticket_request = self.user.ticket_requests.get()

        self.assertTrue(self.user.ticket_requests.exists())
        self.assertTrue(TicketMatch.objects.exists())
        ticket_match = TicketMatch.objects.get()
        self.assertIn(
            reverse('match_confirm', kwargs={'pk': ticket_match.pk}),
            response._headers.get('location', (None, []))[1],
        )
        self.assertTrue(ticket_request.is_reserved)
        self.assertTrue(ticket_offer.is_reserved)

    def test_offer_confirmation(self):
        ticket_offer = self.other_user.ticket_offers.create()
        ticket_request = self.user.ticket_requests.create()
        ticket_match = TicketMatch.objects.create(
            ticket_request=ticket_request,
            ticket_offer=ticket_offer,
        )

        self.assertEqual(len(mail.outbox), 0)

        response = self.client.get(reverse('match_confirm', kwargs={'pk': ticket_match.pk}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('match_confirm', kwargs={'pk': ticket_match.pk}))
        self.assertEqual(response.status_code, 302)

        ticket_offer = TicketOffer.objects.get(pk=ticket_offer.pk)
        ticket_request = TicketRequest.objects.get(pk=ticket_request.pk)
        ticket_match = TicketMatch.objects.get(pk=ticket_match.pk)

        self.assertTrue(ticket_offer.is_fulfilled)
        self.assertTrue(ticket_request.is_fulfilled)
        self.assertTrue(ticket_match.is_accepted)

        self.assertEqual(len(mail.outbox), 2)
        to_addresses = [message.to[0] for message in mail.outbox]
        self.assertIn(self.other_user.email, to_addresses)
        self.assertIn(self.user.email, to_addresses)

    def test_offer_rejection(self):
        ticket_offer = self.other_user.ticket_offers.create()
        ticket_request = self.user.ticket_requests.create()
        ticket_match = TicketMatch.objects.create(
            ticket_request=ticket_request,
            ticket_offer=ticket_offer,
        )

        self.assertEqual(len(mail.outbox), 0)

        response = self.client.get(reverse('match_confirm', kwargs={'pk': ticket_match.pk}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('match_confirm', kwargs={'pk': ticket_match.pk}),
            {'_reject': True},
        )
        self.assertEqual(response.status_code, 302)

        ticket_offer = TicketOffer.objects.get(pk=ticket_offer.pk)
        ticket_request = TicketRequest.objects.get(pk=ticket_request.pk)
        ticket_match = TicketMatch.objects.get(pk=ticket_match.pk)

        self.assertTrue(ticket_offer.is_active)
        self.assertTrue(ticket_request.is_cancelled)
        self.assertTrue(ticket_match.is_terminated)

        self.assertEqual(len(mail.outbox), 0)

    def test_offer_rejection_is_automatched(self):
        ticket_offer = self.other_user.ticket_offers.create()
        ticket_request = self.user.ticket_requests.create()
        ticket_match = TicketMatch.objects.create(
            ticket_request=ticket_request,
            ticket_offer=ticket_offer,
        )
        user3 = User.objects.create(**get_user_kwargs())
        pending_request = user3.ticket_requests.create()

        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(
            reverse('match_confirm', kwargs={'pk': ticket_match.pk}),
            {'_reject': True},
        )
        self.assertEqual(response.status_code, 302)

        ticket_offer = TicketOffer.objects.get(pk=ticket_offer.pk)
        ticket_request = TicketRequest.objects.get(pk=ticket_request.pk)
        ticket_match = TicketMatch.objects.get(pk=ticket_match.pk)

        self.assertTrue(ticket_offer.is_reserved)
        self.assertTrue(pending_request.is_reserved)
        self.assertTrue(ticket_request.is_cancelled)
        self.assertTrue(ticket_match.is_terminated)

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[0].to, user3.email)
