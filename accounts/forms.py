from django import forms
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm, UserCreationForm as DjangoUserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.us import forms as us_forms

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


class NewUserForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    phone_number = us_forms.USPhoneNumberField()

    class Meta:
        model = User
        fields = ('display_name', 'phone_number')
