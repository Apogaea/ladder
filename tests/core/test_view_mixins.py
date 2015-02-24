from django.http import HttpResponse
from django.views.generic import View
from django.test.client import RequestFactory

from rest_framework import status

from ladder.core.decorators import AdminRequiredMixin


class AdminRequiredView(AdminRequiredMixin, View):
    def get(self, *args, **kwargs):
        return HttpResponse('success')


admin_required_view = AdminRequiredView.as_view()


def test_regular_user_denied(factories):
    request_factory = RequestFactory()
    request = request_factory.get('/admin/')
    request.user = factories.UserFactory()

    response = admin_required_view(request)
    assert response.status_code == status.HTTP_302_FOUND


def test_super_user_allowed(factories):
    request_factory = RequestFactory()
    request = request_factory.get('/admin/')
    request.user = factories.SuperUserFactory()

    response = admin_required_view(request)
    assert response.status_code == status.HTTP_200_OK
