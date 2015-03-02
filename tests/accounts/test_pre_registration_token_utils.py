import urlparse

from ladder.apps.accounts.utils import (
    generate_pre_registration_token,
    reverse_pre_registration_url,
    unsign_pre_registration_token,
)


def test_token_generation():
    """
    Verifies that the token round trip works.
    """
    email_in = 'test@example.com'
    token = generate_pre_registration_token(email_in)
    email_out = unsign_pre_registration_token(token)

    assert email_in == email_out


def test_reversing_pre_registration_url():
    email_in = 'test@example.com'
    url = reverse_pre_registration_url(email_in)
    base_url, _, qs = url.partition('?')
    params = urlparse.parse_qs(qs)
    assert 'token' in params
    email_out = unsign_pre_registration_token(params['token'][0])

    assert email_in == email_out
