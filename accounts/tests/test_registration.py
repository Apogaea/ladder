import mock
import urllib

from django.core.urlresolvers import reverse
from django.core import mail
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework import status

from accounts.utils import (
    reverse_registration_url, generate_registration_token, generate_phone_number_code,
)


class InitiateRegistrationTest(TestCase):
    def test_registration_page(self):
        url = reverse('register')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_initiate_registration(self):
        url = reverse('register')
        email, phone_number = 'test@example.com', '5554443333'

        token = generate_registration_token(email, phone_number)
        with mock.patch('django.core.signing.dumps', return_value=token):
            response = self.client.post(url, {
                'email': 'test@example.com',
                'phone_number': '555-444-3333',  # The form takes care of formatting.
            })

            target_url = reverse('register_success')

            self.assertRedirects(response, target_url)
            self.assertEqual(len(mail.outbox), 1)

            message = mail.outbox[0]

        self.assertIn(urllib.quote(token), message.body)

    def test_registration_confirm_page(self):
        email, phone_number = 'test@example.com', '5554443333'
        url = reverse_registration_url(email, phone_number)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['token_valid'])

    def test_registration_confirm_phone_number(self):
        email, phone_number = 'test@example.com', '5554443333'
        url = reverse_registration_url(email, phone_number)

        with mock.patch('accounts.utils.send_twilio_sms') as send_twilio_sms:
            response = self.client.post(url)

        target_url = reverse(
            'register_verify_phone_number',
            kwargs={
                'token': generate_registration_token(email, phone_number),
            },
        )
        self.assertRedirects(response, target_url)
        self.assertTrue(send_twilio_sms.called)

        message = send_twilio_sms.call_args[0][1]

        self.assertIn(
            generate_phone_number_code(phone_number),
            message,
        )

    def test_registration_complete(self):
        email, phone_number = 'test@example.com', '5554443333'
        url = reverse(
            'register_verify_phone_number',
            kwargs={
                'token': generate_registration_token(email, phone_number),
            },
        )
        target_url = reverse('dashboard')

        code = generate_phone_number_code(phone_number)

        response = self.client.post(url, {
            'sms_code': code,
            'display_name': 'test-display_name',
            'password1': 'secret',
            'password2': 'secret',
        })

        self.assertRedirects(response, target_url)

        self.assertTrue(User.objects.filter(email=email).exists())

        user = User.objects.get(email=email)

        self.assertTrue(user.check_password('secret'))
        self.assertTrue(user.is_active)

        self.assertTrue(self.client.login(
            username=user.email,
            password='secret',
        ))

        self.assertTrue(user.is_active)
        self.assertEqual(user.display_name, 'test-display_name')
        self.assertEqual(user.profile.phone_number, phone_number)
