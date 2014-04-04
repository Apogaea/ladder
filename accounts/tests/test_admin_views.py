from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

from rest_framework import status

from accounts.tests.factories import (
    UserWithProfileFactory, SuperUserWithProfileFactory,
)


class WithAuthenticatedSuperUserMixin(object):
    def setUp(self):
        self.super_user = SuperUserWithProfileFactory(password='secret')
        self.assertTrue(self.client.login(
            username=self.super_user.email,
            password='secret',
        ))


class UserIndexTest(WithAuthenticatedSuperUserMixin, TestCase):
    def test_admin_user_index_page(self):
        for i in range(20):
            UserWithProfileFactory()

        response = self.client.get(reverse('admin:user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_detail_page(self):
        user = UserWithProfileFactory()

        response = self.client.get(reverse(
            'admin:user_detail', kwargs={'pk': user.pk},
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_change_user(self):
        user = UserWithProfileFactory(
            _profile__phone_number='555-444-3333',
            email='original@example.com',
            display_name='original',
            is_active=True,
            is_superuser=True,
        )
        url = reverse('admin:user_change', kwargs={'pk': user.pk})

        response = self.client.post(url, {
            'phone_number': '555-555-5555',
            'email': 'test-email@example.com',
            'display_name': 'test-display_name',
            'is_active': False,
            'is_superuser': False,
        })
        self.assertRedirects(
            response,
            reverse('admin:user_detail', kwargs={'pk': user.pk}),
        )

        updated_user = User.objects.get(pk=user.pk)
        self.assertEqual(updated_user.email, 'test-email@example.com')
        self.assertEqual(updated_user.display_name, 'test-display_name')
        self.assertEqual(updated_user.profile.phone_number, '555-555-5555')
        self.assertFalse(updated_user.is_active)
        self.assertFalse(updated_user.is_superuser)
