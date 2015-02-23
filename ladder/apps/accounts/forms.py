from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

from localflavor.us.forms import USPhoneNumberField

from betterforms.forms import BetterForm, BetterModelForm

from ladder.apps.accounts.utils import generate_phone_number_code


class InitiateRegistrationForm(BetterForm):
    error_messages = {
        "duplicate_email": "A user with that email address already exists",
        "duplicate_phone_number": "A user with that phone number address already exists",
    }
    email = forms.EmailField()
    phone_number = USPhoneNumberField()

    def clean_email(self):
        User = get_user_model()
        email = self.cleaned_data['email']

        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email
        else:
            raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        try:
            User.objects.get(_profile__phone_number=phone_number)
        except User.DoesNotExist:
            return phone_number
        else:
            raise forms.ValidationError(self.error_messages['duplicate_phone_number'])


class UserChangeForm(BetterModelForm):
    class Meta:
        model = User
        fields = ('display_name',)


class UserCreationForm(BetterModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'duplicate_username': "A user with that %(username)s already exists.",
    }
    sms_code = forms.CharField(label="SMS Code")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as above,"
                                          " for verification.")

    def __init__(self, *args, **kwargs):
        self.phone_number = kwargs.pop('phone_number')
        super(UserCreationForm, self).__init__(*args, **kwargs)

    def clean_sms_code(self):
        code = self.cleaned_data['sms_code']
        if not code == generate_phone_number_code(self.phone_number):
            raise forms.ValidationError('Incorrect Code')

    def clean(self):
        super(UserCreationForm, self).clean()
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])

    class Meta:
        model = User
        fields = ('display_name',)

    def save(self, commit=True):
        self.instance.set_password(self.cleaned_data["password1"])
        return super(UserCreationForm, self).save(commit)
