import pytest

from django.core.urlresolvers import reverse

from rest_framework import status

from ladder.apps.accounts.utils import (
    reverse_pre_registration_url,
)


@pytest.mark.django_db
def test_pre_registration_with_token(client, mocker, before_registration_window):
    url = reverse_pre_registration_url('test@example.com')
    email = 'test@example.com'
    phone_number = '5554443333'

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_pre_registration_with_incorrect_email_address(client, mocker,
                                                       before_registration_window):
    url = reverse_pre_registration_url('test@example.com')
    email = 'test@example.com'
    phone_number = '5554443333'

    response = client.post(url, {
        'email': 'wrong-email@example.com',
        'phone_number': '555-444-3333',  # The form takes care of formatting.
    })

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_pre_registration_with_correct_email_addess(client, mocker,
                                                    before_registration_window):
    url = reverse_pre_registration_url('test@example.com')
    email = 'test@example.com'
    phone_number = '5554443333'

    response = client.post(url, {
        'email': email,
        'phone_number': '555-444-3333',  # The form takes care of formatting.
    })

    assert response.status_code == status.HTTP_302_FOUND
