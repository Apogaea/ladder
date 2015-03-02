import pytest

from django.core.urlresolvers import reverse

from rest_framework import status


@pytest.mark.django_db
def test_initiate_registration_before_window(client, mocker, before_registration_window):
    url = reverse('register')
    email = 'test@example.com'
    phone_number = '5554443333'

    get_response = client.get(url)

    post_response = client.post(url, {
        'email': 'test@example.com',
        'phone_number': '555-444-3333',  # The form takes care of formatting.
    })

    assert get_response.status_code == status.HTTP_302_FOUND
    assert post_response.status_code == status.HTTP_302_FOUND

    expected_url = reverse('registration-closed')

    assert get_response.get('location', '').endswith(expected_url)
    assert post_response.get('location', '').endswith(expected_url)


@pytest.mark.django_db
def test_initiate_registration_after_window(client, mocker, after_registration_window):
    url = reverse('register')
    email = 'test@example.com'
    phone_number = '5554443333'

    get_response = client.get(url)

    post_response = client.post(url, {
        'email': 'test@example.com',
        'phone_number': '555-444-3333',  # The form takes care of formatting.
    })

    assert get_response.status_code == status.HTTP_302_FOUND
    assert post_response.status_code == status.HTTP_302_FOUND

    expected_url = reverse('registration-closed')

    assert get_response.get('location', '').endswith(expected_url)
    assert post_response.get('location', '').endswith(expected_url)
