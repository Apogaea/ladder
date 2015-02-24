import pytest
import urllib

from django.core.urlresolvers import reverse
from django.core import mail

from rest_framework import status

from ladder.apps.accounts.utils import (
    reverse_registration_url, generate_registration_token, generate_phone_number_code,
)


def test_registration_page(client):
    url = reverse('register')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_initiate_registration(client, mocker):
    url = reverse('register')
    email = 'test@example.com'
    phone_number = '5554443333'

    token = generate_registration_token(email, phone_number)

    mocker.patch('django.core.signing.dumps', return_value=token)

    response = client.post(url, {
        'email': 'test@example.com',
        'phone_number': '555-444-3333',  # The form takes care of formatting.
    })

    target_url = reverse('register-success')

    assert response.get('location', '').endswith(target_url)
    assert len(mail.outbox) == 1

    message = mail.outbox[0]

    assert urllib.quote(token) in message.body


@pytest.mark.django_db
def test_registration_confirm_page(client):
    email = 'test@example.com'
    phone_number = '5554443333'

    url = reverse_registration_url(email, phone_number)

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'form' in response.context
    assert response.context['token_valid']


@pytest.mark.django_db
def test_registration_confirm_phone_number(client, mocker):
    email = 'test@example.com'
    phone_number = '5554443333'

    url = reverse_registration_url(email, phone_number)

    send_twilio_sms = mocker.patch('ladder.apps.accounts.utils.send_twilio_sms')

    response = client.post(url)

    target_url = reverse(
        'register-verify-phone-number',
        kwargs={
            'token': generate_registration_token(email, phone_number),
        },
    )
    assert response.get('location', '').endswith(target_url)
    assert send_twilio_sms.called

    message = send_twilio_sms.call_args[0][1]

    code = generate_phone_number_code(phone_number)
    formatted_code = "{0} {1}".format(code[:3], code[3:])
    assert formatted_code in message


@pytest.mark.django_db
def test_registration_complete(User, client):
    email = 'test@example.com'
    phone_number = '5554443333'

    url = reverse(
        'register-verify-phone-number',
        kwargs={
            'token': generate_registration_token(email, phone_number),
        },
    )
    target_url = reverse('dashboard')

    code = generate_phone_number_code(phone_number)

    response = client.post(url, {
        'sms_code': code,
        'display_name': 'test-display_name',
        'password': 'secret',
    })

    assert response.get('location', '').endswith(target_url)

    assert User.objects.filter(email=email).exists()

    user = User.objects.get(email=email)

    assert user.check_password('secret')
    assert user.is_active

    assert client.login(
        username=user.email,
        password='secret',
    )

    assert user.is_active
    assert user.display_name == 'test-display_name'
    assert user.profile.phone_number == phone_number
