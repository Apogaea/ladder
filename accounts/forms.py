from django import forms

from authtools.forms import UserCreationForm as AuthToolsUserCreationForm

from accounts.models import User


class UserCreationForm(AuthToolsUserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ('email', 'display_name', 'phone_number',)
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'XXX-XXX-XXXX'}),
        }


class UserChangeForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ('display_name', 'phone_number')
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'XXX-XXX-XXXX'}),
        }
