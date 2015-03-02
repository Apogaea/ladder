import pytest

from django.core.urlresolvers import reverse

from rest_framework import status


@pytest.mark.django_db
def test_pre_registration_with_token(client, mocker, before_registration_window):
    url = reverse('registration-closed')

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
