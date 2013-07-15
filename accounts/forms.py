from django import forms

from accounts.models import User


class UserCreationForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ('email', 'display_name',)


class UserChangeForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ('display_name',)
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'XXX-XXX-XXXX'}),
        }
