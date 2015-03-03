import urllib

import pytest

from django.core.urlresolvers import reverse
from django.core import mail

from rest_framework import status

from ladder.apps.accounts.utils import (
    generate_pre_registration_token,
    reverse_pre_registration_url,
    reverse_registration_url,
    generate_registration_token,
    generate_phone_number_code,
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


@pytest.mark.django_db
def test_pre_registration_email_contains_token(client, mocker,
                                               before_registration_window):
    token = generate_pre_registration_token('test@example.com')
    url = reverse_pre_registration_url('test@example.com', token=token)
    email = 'test@example.com'
    phone_number = '5554443333'

    response = client.post(url, {
        'email': email,
        'phone_number': '555-444-3333',  # The form takes care of formatting.
    })

    assert response.status_code == status.HTTP_302_FOUND

    message = mail.outbox[0]
    p1, p2, p3 = token.split(':')
    assert p1 in message.body
    assert p2 in message.body
    assert p3 in message.body


@pytest.mark.django_db
def test_pre_registration_send_sms_code(client, mocker, User,
                                        before_registration_window):
    email = 'test@example.com'
    phone_number = '5554443333'
    token = generate_pre_registration_token(email)

    url = reverse_registration_url(email, phone_number)
    url = '?'.join((
        url,
        urllib.urlencode({'token': token}),
    ))
    target_url = reverse('dashboard')

    send_twilio_sms = mocker.patch('ladder.apps.accounts.utils.send_twilio_sms')

    response = client.post(url)

    target_url = reverse(
        'register-verify-phone-number',
        kwargs={
            'token': generate_registration_token(email, phone_number),
        },
    )
    target_url = '?'.join((
        target_url,
        urllib.urlencode({'token': token}),
    ))
    assert response.get('location', '').endswith(target_url)


@pytest.mark.django_db
def test_pre_registration_phone_confirmation_step(client, mocker, User,
                                                  before_registration_window):
    email = 'test@example.com'
    phone_number = '5554443333'

    token = generate_pre_registration_token(email)

    url = reverse(
        'register-verify-phone-number',
        kwargs={
            'token': generate_registration_token(email, phone_number),
        },
    )
    url = '?'.join((
        url,
        urllib.urlencode({'token': token}),
    ))
    target_url = reverse('dashboard')

    code = generate_phone_number_code(phone_number)

    response = client.post(url, {
        'sms_code': code,
        'display_name': 'test-display_name',
        'password': 'secret',
    })

    assert response.get('location', '').endswith(target_url)
    assert User.objects.filter(email=email).exists()
