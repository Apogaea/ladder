from django.test import TestCase

from accounts.forms import InitiateRegistrationForm
from accounts.tests.factories import UserWithProfileFactory


class InitiateRegistrationFormTest(TestCase):
    def test_email_uniqueness_validation(self):
        user = UserWithProfileFactory()

        form = InitiateRegistrationForm({
            'email': user.email,
            'phone_number': '555-222-3333',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn(
            InitiateRegistrationForm.error_messages['duplicate_email'],
            form.errors['email'],
        )

    def test_phone_number_uniqueness_validation(self):
        user = UserWithProfileFactory()

        form = InitiateRegistrationForm({
            'email': 'unique1234@example.com',
            'phone_number': user.profile.phone_number,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertIn(
            InitiateRegistrationForm.error_messages['duplicate_phone_number'],
            form.errors['phone_number'],
        )

    def test_phone_number_normalized(self):
        formats = (
            '(555) 444 3322',
            '5554443322',
            '555.444.3322',
            '555-444-3322',
            '555 444 3322',
        )
        email = 'test@example.com'
        forms = [
            InitiateRegistrationForm({
                'email': email,
                'phone_number': phone_number,
            }) for phone_number in formats
        ]
        self.assertTrue(all(form.is_valid() for form in forms))

        cleaned_values = [form.cleaned_data['phone_number'] for form in forms]

        self.assertEqual(len(set(cleaned_values)), 1)
        self.assertEqual(cleaned_values[0], '555-444-3322')
