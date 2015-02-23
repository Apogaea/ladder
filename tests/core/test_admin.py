from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework import status

from accounts.tests.factories import SuperUserFactory, UserFactory


class AdminLoginTest(TestCase):
    def setUp(self):
        super(AdminLoginTest, self).setUp()
        self.url = reverse('admin:login')

    def test_page_with_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context)

    def test_page_with_authenticated_regular_user(self):
        user = UserFactory(password='secret')
        self.assertTrue(self.client.login(
            username=user.email,
            password='secret',
        ))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context)

    def test_page_with_authenticated_admin(self):
        user = SuperUserFactory(password='secret')
        self.assertTrue(self.client.login(
            username=user.email,
            password='secret',
        ))
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('admin:index'))

    def test_authentication_by_superuser(self):
        user = SuperUserFactory(password='secret')
        response = self.client.post(self.url, {
            'username': user.email,
            'password': 'secret',
        })
        self.assertRedirects(response, reverse('admin:index'))

    def test_authentication_noop_by_unauthenticated_normal_user(self):
        user = UserFactory(password='secret')
        response = self.client.post(self.url, {
            'username': user.email,
            'password': 'secret',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AdminIndexTest(TestCase):
    def test_page(self):
        user = SuperUserFactory(password='secret')
        self.assertTrue(self.client.login(
            username=user.email,
            password='secret',
        ))

        response = self.client.get(reverse('admin:index'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
