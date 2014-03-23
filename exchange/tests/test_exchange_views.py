from __future__ import division

from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

from accounts.tests.factories import UserWithProfileFactory

from exchange.models import (
    TicketRequest, TicketOffer, TicketMatch,
)
from exchange.tests.factories import (
    TicketRequestFactory, TicketOfferFactory, TicketMatchFactory,
)

User = get_user_model()


class TestExchangeRequestAndOfferViews(TestCase):
    def setUp(self):
        self.user = UserWithProfileFactory(password='secret')
        self.client.login(email=self.user.email, password='secret')

    def test_automatic_offer_creation_view(self):
        ticket_request = TicketRequestFactory()

        response = self.client.get(reverse('offer_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(self.user.ticket_offers.exists())
        self.assertFalse(TicketMatch.objects.exists())
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(reverse('offer_create'), {'is_automatch': True})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertTrue(self.user.ticket_offers.exists())
        self.assertTrue(TicketMatch.objects.exists())

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[0].to, ticket_request.user.email)

    def test_manual_offer_creation_doesnt_auto_match(self):
        ticket_request = TicketRequestFactory()

        response = self.client.get(reverse('offer_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(self.user.ticket_offers.exists())
        self.assertFalse(TicketMatch.objects.exists())
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(reverse('offer_create'), {'is_automatch': False})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertTrue(self.user.ticket_offers.exists())
        self.assertFalse(TicketMatch.objects.exists())

        ticket_offer = self.user.ticket_offers.get()

        self.assertTrue(ticket_offer.is_active)
        self.assertTrue(ticket_request.is_active)

        self.assertEqual(len(mail.outbox), 0)

    def test_request_creation_view(self):
        response = self.client.get(reverse('request_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(self.user.ticket_requests.exists())

        response = self.client.post(
            reverse('request_create'), {'message': 'A nice heartfelt message'},
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertTrue(self.user.ticket_requests.exists())

    def test_automatic_request_matching(self):
        TicketOfferFactory(is_automatch=True)

        self.assertFalse(self.user.ticket_requests.exists())
        self.assertFalse(TicketMatch.objects.exists())

        response = self.client.post(
            reverse('request_create'), {'message': 'A nice heartfelt message'},
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertTrue(self.user.ticket_requests.exists())
        self.assertTrue(TicketMatch.objects.exists())
        ticket_match = TicketMatch.objects.get()
        self.assertRedirects(
            response, reverse('match_confirm', kwargs={'pk': ticket_match.pk}),
        )

    def test_offer_confirmation(self):
        ticket_match = TicketMatchFactory(
            ticket_request__user=self.user,
        )

        self.assertEqual(len(mail.outbox), 0)

        response = self.client.get(reverse('match_confirm', kwargs={'pk': ticket_match.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(reverse('match_confirm', kwargs={'pk': ticket_match.pk}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        ticket_offer = TicketOffer.objects.get(pk=ticket_match.ticket_offer.pk)
        ticket_request = TicketRequest.objects.get(pk=ticket_match.ticket_request.pk)
        ticket_match = TicketMatch.objects.get(pk=ticket_match.pk)

        self.assertTrue(ticket_offer.is_fulfilled)
        self.assertTrue(ticket_request.is_fulfilled)
        self.assertTrue(ticket_match.is_accepted)

        self.assertEqual(len(mail.outbox), 2)
        to_addresses = [message.to[0] for message in mail.outbox]
        self.assertIn(ticket_offer.user.email, to_addresses)
        self.assertIn(self.user.email, to_addresses)

    def test_offer_rejection(self):
        ticket_match = TicketMatchFactory(
            ticket_request__user=self.user,
        )

        self.assertEqual(len(mail.outbox), 0)

        response = self.client.get(reverse('match_confirm', kwargs={'pk': ticket_match.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            reverse('match_confirm', kwargs={'pk': ticket_match.pk}),
            {'_reject': True},
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        ticket_offer = TicketOffer.objects.get(pk=ticket_match.ticket_offer.pk)
        ticket_request = TicketRequest.objects.get(pk=ticket_match.ticket_request.pk)
        ticket_match = TicketMatch.objects.get(pk=ticket_match.pk)

        self.assertTrue(ticket_offer.is_active)
        self.assertTrue(ticket_request.is_cancelled)
        self.assertTrue(ticket_match.is_terminated)

        self.assertEqual(len(mail.outbox), 0)

    def test_offer_rejection_is_automatched(self):
        ticket_match = TicketMatchFactory(
            ticket_request__user=self.user,
        )

        pending_request = TicketRequestFactory()

        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(
            reverse('match_confirm', kwargs={'pk': ticket_match.pk}),
            {'_reject': True},
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        ticket_offer = TicketOffer.objects.get(pk=ticket_match.ticket_offer.pk)
        ticket_request = TicketRequest.objects.get(pk=ticket_match.ticket_request.pk)
        ticket_match = TicketMatch.objects.get(pk=ticket_match.pk)

        self.assertTrue(ticket_offer.is_reserved)
        self.assertTrue(pending_request.is_reserved)
        self.assertTrue(ticket_request.is_cancelled)
        self.assertTrue(ticket_match.is_terminated)

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[0].to, pending_request.user.email)


class TicketOfferManagementTest(TestCase):
    def setUp(self):
        super(TicketOfferManagementTest, self).setUp()
        self.user = UserWithProfileFactory(password='secret')
        self.assertTrue(self.client.login(
            username=self.user.email,
            password='secret',
        ))

    def test_cancel_offer_page(self):
        offer = TicketOfferFactory(user=self.user)

        url = reverse('offer_cancel', kwargs={'pk': offer.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_canceling_an_offer(self):
        offer = TicketOfferFactory(user=self.user)

        url = reverse('offer_cancel', kwargs={'pk': offer.pk})

        response = self.client.post(url)

        self.assertRedirects(response, reverse('dashboard'))

        cancelled_offer = TicketOffer.objects.get(pk=offer.pk)
        self.assertTrue(cancelled_offer.is_cancelled)

    def test_toggle_automatch_page(self):
        offer = TicketOfferFactory(user=self.user, is_automatch=False)

        url = reverse('offer_toggle_automatch', kwargs={'pk': offer.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_turning_on_automatch(self):
        offer = TicketOfferFactory(user=self.user, is_automatch=False)

        url = reverse('offer_toggle_automatch', kwargs={'pk': offer.pk})

        response = self.client.post(url)

        self.assertRedirects(response, reverse('offer_detail', kwargs={'pk': offer.pk}))

        updated_offer = TicketOffer.objects.get(pk=offer.pk)
        self.assertTrue(updated_offer.is_automatch)

    def test_turning_off_automatch(self):
        offer = TicketOfferFactory(user=self.user, is_automatch=True)

        url = reverse('offer_toggle_automatch', kwargs={'pk': offer.pk})

        response = self.client.post(url)

        self.assertRedirects(response, reverse('offer_select_recipient', kwargs={'pk': offer.pk}))

        updated_offer = TicketOffer.objects.get(pk=offer.pk)
        self.assertFalse(updated_offer.is_automatch)


class TicketRequestManagementTest(TestCase):
    def setUp(self):
        super(TicketRequestManagementTest, self).setUp()
        self.user = UserWithProfileFactory(password='secret')
        self.assertTrue(self.client.login(
            username=self.user.email,
            password='secret',
        ))

    def test_cancel_request_page(self):
        request = TicketRequestFactory(user=self.user)

        url = reverse('request_cancel', kwargs={'pk': request.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cancelling_request(self):
        request = TicketRequestFactory(user=self.user)

        url = reverse('request_cancel', kwargs={'pk': request.pk})

        response = self.client.post(url)

        self.assertRedirects(response, reverse('dashboard'))
        updated_request = TicketRequest.objects.get(pk=request.pk)
        self.assertTrue(updated_request.is_cancelled)

    def test_match_confirm_page(self):
        request = TicketRequestFactory(user=self.user)
        match = TicketMatchFactory(ticket_request=request)

        url = reverse('match_confirm', kwargs={'pk': match.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
