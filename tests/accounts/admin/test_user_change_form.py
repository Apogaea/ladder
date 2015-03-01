from ladder.apps.accounts.admin.forms import (
    UserChangeForm,
)


def test_form_data_initialization(factories):
    user = factories.UserWithProfileFactory(
        email='test-email@example.com',
        display_name='test-display_name',
        _profile__phone_number='555-444-3333',
        _profile__max_allowed_matches=3,
        is_active=False,
        is_staff=True,
    )

    form = UserChangeForm(instance=user)
    assert form.initial['email'] == user.email
    assert form.initial['display_name'] == user.display_name
    assert form.initial['is_active'] == user.is_active
    assert form.initial['is_staff'] == user.is_staff
    assert form.initial['phone_number'] == user.profile.phone_number
    assert form.initial['max_allowed_matches'] == user.profile.max_allowed_matches
