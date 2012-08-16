import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm, UserCreationForm as DjangoUserCreationForm
from django.utils.translation import ugettext_lazy as _
#from django.contrib.localflavor.us import forms as us_forms
#from django.core.exceptions import ValidationError

from ladder.forms import CssForm, CssModelForm

from accounts.models import User


class AuthenticationForm(DjangoAuthenticationForm):
    error_css_class = 'error'
    required_css_class = 'required'

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'tabindex': '50'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'tabindex': '51'}))


class UserCreationForm(DjangoUserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'

    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Email (optional)', 'tabindex': '41'}))
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")},
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'tabindex': '40'}))
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'tabindex': '42'}))
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput(attrs={'tabindex': '43'}),
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ('username', 'email',)


class UserForm(CssModelForm):
    class Meta:
        model = User
        fields = ('display_name', 'phone_number')
        widgets = {
                'phone_number': forms.TextInput(attrs={'placeholder': 'XXX-XXX-XXXX'}),
                }

    def save(self, commit=True):
        original = User.objects.get(pk=self.instance.pk)
        user = super(UserForm, self).save(commit=False)
        if not original.phone_number == user.phone_number:
            user.codes.all().delete()
            user.is_verified = False
            user.verified_at = None
        if commit:
            user.save()
        return user


class PhoneNumberForm(CssModelForm):
    class Meta:
        model = User
        fields = ('display_name', 'phone_number')


class PhoneVerificationForm(CssForm):
    verification_code = forms.CharField(label="Verification Code:")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PhoneVerificationForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_verification_code(self):
        code = self.cleaned_data.get('verification_code')
        code = re.sub(r'[^\d]+', '', code)

        return code
