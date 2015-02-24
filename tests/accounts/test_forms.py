import pytest

from ladder.apps.accounts.forms import InitiateRegistrationForm


def test_email_uniqueness_validation(factories):
    user = factories.UserWithProfileFactory()

    form = InitiateRegistrationForm({
        'email': user.email,
        'phone_number': '555-222-3333',
    })

    assert not form.is_valid()
    assert 'email' in form.errors
    assert InitiateRegistrationForm.error_messages['duplicate_email'] in form.errors['email']


def test_phone_number_uniqueness_validation(factories):
    user = factories.UserWithProfileFactory()

    form = InitiateRegistrationForm({
        'email': 'unique1234@example.com',
        'phone_number': user.profile.phone_number,
    })

    assert not form.is_valid()
    assert 'phone_number' in form.errors
    assert InitiateRegistrationForm.error_messages['duplicate_phone_number'] in form.errors['phone_number']


@pytest.mark.django_db
@pytest.mark.parametrize(
    "phone_number",
    (
        '(555) 444 3322',
        '5554443322',
        '555.444.3322',
        '555-444-3322',
        '555 444 3322',
    ),
)
def test_phone_number_normalized(phone_number):
    email = 'test@example.com'
    form = InitiateRegistrationForm({
        'email': email,
        'phone_number': phone_number,
    })
    assert form.is_valid()

    assert form.cleaned_data['phone_number'] == '555-444-3322'
