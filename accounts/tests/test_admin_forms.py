from django.test import TestCase

from accounts.tests.factories import UserWithProfileFactory
from accounts.admin.forms import UserChangeForm


class UserChangeFormTest(TestCase):
    def test_email_uniqueness_enforcement(self):
        user = UserWithProfileFactory()
        other_user = UserWithProfileFactory(email='taken@example.com')

        data = {
            'email': other_user.email,
            'display_name': user.display_name,
            'phone_number': user.profile.phone_number,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
        }

        form = UserChangeForm(data, instance=user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_phone_number_uniqueness_enforcement(self):
        user = UserWithProfileFactory()
        other_user = UserWithProfileFactory(
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
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
