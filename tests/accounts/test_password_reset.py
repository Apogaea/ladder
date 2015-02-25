import pytest

from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.forms import (
    urlsafe_base64_encode,
    default_token_generator,
)
from django.utils.encoding import force_bytes

from rest_framework import status


@pytest.mark.django_db
def test_password_reset_page(client):
    response = client.get(reverse('password-reset'))

    assert response.status_code == status.HTTP_200_OK


def test_initiate_password_reset(client, factories):
    user = factories.UserWithProfileFactory()

    response = client.post(reverse('password-reset'), {
        'email': user.email,
    })

    assert response.get('location', '').endswith(reverse('password-reset-done'))
    assert len(mail.outbox) == 1


def test_password_reset_confirm_page(client, factories):
    user = factories.UserWithProfileFactory()
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    response = client.get(reverse(
        'password-reset-confirm-and-login',
        kwargs={
            'uidb64': uidb64,
            'token': token,
        },
    ))
    assert response.status_code == status.HTTP_200_OK
    assert response.context['validlink']


def test_password_reset_confirming(client, factories, User):
    user = factories.UserWithProfileFactory(password='secret')
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    url = reverse(
        'password-reset-confirm-and-login',
        kwargs={
            'uidb64': uidb64,
            'token': token,
        },
    )
    response = client.post(url, {
        'new_password1': 'new-secret',
        'new_password2': 'new-secret',
    })
    assert response.get('location', '').endswith(reverse('dashboard'))

    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.check_password('new-secret')
