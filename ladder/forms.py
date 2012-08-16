from django import forms


class CssModelForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'


class CssForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
