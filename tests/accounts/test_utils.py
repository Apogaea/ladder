import datetime
import urllib
import mock

from django.test import TestCase


from accounts.utils import (
    reverse_registration_url, unsign_registration_token,
    generate_registration_token, generate_phone_number_code,
)


class PhoneNumberCodeTest(TestCase):
    def test_code_generation(self):
        now = datetime.datetime.now()

        with mock.patch('datetime.datetime', now=mock.Mock(return_value=now)):
            phone_number = '555-444-3333'
            code = generate_phone_number_code(phone_number)

            self.assertEqual(
                code,
                generate_phone_number_code(phone_number),
            )
            self.assertEqual(len(code), 6)
            self.assertTrue(code.isdigit())

    def test_expiration(self):
        now = datetime.datetime.now()
        now_plus_one_hour = now + datetime.timedelta(seconds=60 * 60)

        with mock.patch('datetime.datetime', now=mock.Mock(return_value=now)):
            phone_number = '555-444-3333'
            code = generate_phone_number_code(phone_number)

        with mock.patch('datetime.datetime', now=mock.Mock(return_value=now_plus_one_hour)):
            self.assertNotEqual(
                code,
                generate_phone_number_code(phone_number),
            )

    def test_zero_padding(self):
        with mock.patch('django.core.signing.Signer.sign') as sign:
            sign.return_value = mock.Mock(__hash__=mock.Mock(return_value=0))
            code = generate_phone_number_code('555-444-3333')

        self.assertEqual(code, '000000')


class RegistrationTokenTest(TestCase):
    def test_token_generation(self):
        email, phone = 'test@example.com', '555-444-3333'
        token = generate_registration_token(email, phone)

        self.assertTrue(token)

        unsigned_email, unsigned_phone = unsign_registration_token(token)
        self.assertEqual(unsigned_email, email)
        self.assertEqual(unsigned_phone, phone)


class RegistrationLinkReversalTest(TestCase):
    def test_registration_link_reversing(self):
        email, phone = 'test@example.com', '555-444-3333'
        token = generate_registration_token(email, phone)
        path = reverse_registration_url(email, phone)

        self.assertIn(urllib.quote(token), path)
