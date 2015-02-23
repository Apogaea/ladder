from django.core.urlresolvers import reverse
from django.core import mail
from django.test import TestCase
from django.contrib.auth.forms import urlsafe_base64_encode, default_token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes

User = get_user_model()

from rest_framework import status

from accounts.tests.factories import UserWithProfileFactory


class PasswordResetTest(TestCase):
    def test_password_reset_page(self):
        response = self.client.get(reverse('password_reset'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_initiate_password_reset(self):
        user = UserWithProfileFactory()

        response = self.client.post(reverse('password_reset'), {
            'email': user.email,
        })

        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)

    def test_password_reset_confirm_page(self):
        user = UserWithProfileFactory()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        response = self.client.get(reverse(
            'password_reset_confirm_and_login',
            kwargs={
                'uidb64': uidb64,
                'token': token,
            },
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.context['validlink'])

    def test_password_reset_confirming(self):
        user = UserWithProfileFactory(password='secret')
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        url = reverse(
            'password_reset_confirm_and_login',
            kwargs={
                'uidb64': uidb64,
                'token': token,
            },
        )
        response = self.client.post(url, {
            'new_password1': 'new-secret',
            'new_password2': 'new-secret',
        })
        self.assertRedirects(response, reverse('dashboard'))

        updated_user = User.objects.get(pk=user.pk)
        self.assertTrue(updated_user.check_password('new-secret'))
