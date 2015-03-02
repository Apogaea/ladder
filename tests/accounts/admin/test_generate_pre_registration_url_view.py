import pytest

from django.core.urlresolvers import reverse

from rest_framework import status


@pytest.mark.django_db
def test_pre_registration_with_token(admin_client, mocker, before_registration_window):
    url = reverse('admin:generate-pre-registration-url')

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'token_url' not in response.context


@pytest.mark.django_db
def test_pre_registration_with_token(admin_client, mocker, before_registration_window):
    url = reverse('admin:generate-pre-registration-url')

    response = admin_client.post(url, {'email': 'test@example.com'})

    assert response.status_code == status.HTTP_200_OK
    assert 'token_url' in response.context
