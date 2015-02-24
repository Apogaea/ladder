from django import forms
from django.contrib.auth import get_user_model

from localflavor.us.forms import USPhoneNumberField

from betterforms.forms import BetterModelForm
from betterforms.changelist import SearchForm

User = get_user_model()


class UserChangeListForm(SearchForm):
    SEARCH_FIELDS = ('email', 'display_name')
    model = User


class UserChangeForm(BetterModelForm):
    error_messages = {
        "duplicate_email": "A user with that email address already exists",
        "duplicate_phone_number": "A user with that phone number address already exists",
    }
    phone_number = USPhoneNumberField()

    class Meta:
        model = User
        fields = ('email', 'display_name', 'is_active', 'is_superuser')

    def clean_email(self):
        User = get_user_model()
        email = self.cleaned_data['email']

        try:
            User.objects.exclude(
                email__iexact=self.instance.email,
            ).get(email__iexact=email)
        except User.DoesNotExist:
            return email
        else:
            raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        try:
            User.objects.exclude(
                _profile__phone_number=self.instance.profile.phone_number,
            ).get(_profile__phone_number=phone_number)
        except User.DoesNotExist:
            return phone_number
        else:
            raise forms.ValidationError(self.error_messages['duplicate_phone_number'])
