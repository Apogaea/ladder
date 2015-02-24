import datetime
import urllib
import mock

from ladder.apps.accounts.utils import (
    reverse_registration_url,
    unsign_registration_token,
    generate_registration_token,
    generate_phone_number_code,
)


def test_code_generation(frozen_now):
    phone_number = '555-444-3333'
    code = generate_phone_number_code(phone_number)

    assert code == generate_phone_number_code(phone_number)
    assert len(code) == 6
    assert code.isdigit()


def test_expiration(frozen_now, mocker):
    now_plus_one_hour = frozen_now + datetime.timedelta(seconds=60 * 60)

    phone_number = '555-444-3333'
    code = generate_phone_number_code(phone_number)

    mocker.stopall()
    mocker.patch('datetime.datetime', now=mock.Mock(return_value=now_plus_one_hour))
    assert not code == generate_phone_number_code(phone_number)


def test_zero_padding(mocker):
    mocker.patch(
        'django.core.signing.Signer.sign',
        return_value=mock.Mock(__hash__=mock.Mock(return_value=5)),
    )
    code = generate_phone_number_code('555-444-3333')

    assert code == '000005'


def test_token_unsigning():
    email = 'test@example.com'
    phone = '555-444-3333'
    token = generate_registration_token(email, phone)

    assert token

    unsigned_email, unsigned_phone = unsign_registration_token(token)
    assert unsigned_email == email
    assert unsigned_phone == phone


def test_registration_link_reversing():
    email = 'test@example.com'
    phone = '555-444-3333'
    token = generate_registration_token(email, phone)
    path = reverse_registration_url(email, phone)

    assert urllib.quote(token) in path
