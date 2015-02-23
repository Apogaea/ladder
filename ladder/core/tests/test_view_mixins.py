from django.test import TestCase
from django.http import HttpResponse
from django.views.generic import View
from django.test.client import RequestFactory

from rest_framework import status

from accounts.tests.factories import SuperUserFactory, UserFactory

from ladder.decorators import AdminRequiredMixin


class AdminRequiredView(AdminRequiredMixin, View):
    def get(self, *args, **kwargs):
        return HttpResponse('success')


admin_required_view = AdminRequiredView.as_view()


class AdminRequiredMixinTest(TestCase):
    def setUp(self):
        super(AdminRequiredMixinTest, self).setUp()
        self.factory = RequestFactory()
        self.super_user = SuperUserFactory

    def test_regular_user_denied(self):
        request = self.factory.get('/admin/')
        request.user = UserFactory()

        response = admin_required_view(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_super_user_allowed(self):
        request = self.factory.get('/admin/')
        request.user = SuperUserFactory()

        response = admin_required_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
