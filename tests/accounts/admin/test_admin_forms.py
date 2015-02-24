from ladder.apps.accounts.admin.forms import UserChangeForm


def test_email_uniqueness_enforcement(factories):
    user = factories.UserWithProfileFactory()
    other_user = factories.UserWithProfileFactory(email='taken@example.com')

    data = {
        'email': other_user.email,
        'display_name': user.display_name,
        'phone_number': user.profile.phone_number,
        'is_active': user.is_active,
        'is_superuser': user.is_superuser,
    }

    form = UserChangeForm(data, instance=user)
    assert not form.is_valid()
    assert 'email' in form.errors


def test_phone_number_uniqueness_enforcement(factories):
    user = factories.UserWithProfileFactory()
    other_user = factories.UserWithProfileFactory(
        _profile__phone_number='555-555-5555',
    )

    data = {
        'email': user.email,
        'display_name': user.display_name,
        'phone_number': other_user.profile.phone_number,
        'is_active': user.is_active,
        'is_superuser': user.is_superuser,
    }

    form = UserChangeForm(data, instance=user)
    assert not form.is_valid()
    assert 'phone_number' in form.errors
