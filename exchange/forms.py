from django import forms
from django.utils import timezone

from fusionbox.forms import BaseModelForm, BaseForm

from exchange.models import (
    TicketOffer, TicketRequest, TicketMatch, PhoneNumber,
)


class TicketOfferForm(BaseModelForm):
    """
    Form for creating a ticket offer.
    """
    class Meta:
        model = TicketOffer
        fields = ('is_automatch',)


class TicketRequestForm(BaseModelForm):
    """
    Form for creating a ticket request.
    """
    class Meta:
        model = TicketRequest
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'ng-model': 'message'}),
        }


class SelectTicketRequestForm(BaseForm):
    """
    Form for presenting a user with a choice of ticket requests to fulfill.
    """
    ticket_request = forms.ModelChoiceField(queryset=TicketRequest.objects.none())


class NoFieldsTicketOfferForm(BaseModelForm):
    class Meta:
        model = TicketMatch
        fields = tuple()


class NoFieldsTicketRequestForm(BaseModelForm):
    class Meta:
        model = TicketRequest
        fields = tuple()


class NoFieldsTicketMatchForm(BaseModelForm):
    class Meta:
        model = TicketMatch
        fields = tuple()


class PhoneNumberForm(BaseModelForm):
    class Meta:
        model = PhoneNumber
        fields = ('phone_number',)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if PhoneNumber.objects.is_verified().exclude(pk=self.instance.pk).filter(phone_number=phone_number).exists():
            raise forms.ValidationError('That phone number is already associated with an account')

        return phone_number


class VerifyPhoneNumberForm(BaseModelForm):
    code = forms.CharField(label='Confirmation Code')

    class Meta:
        model = PhoneNumber
        fields = tuple()

    def clean_code(self):
        code = self.cleaned_data['code']
        # strip whitespace
        code = code.strip()
        # remove any dashes
        code = code.replace('-', '')

        if not code == self.instance.confirmation_code:
            raise forms.ValidationError('Incorrect confirmation code')
        return code

    def save(self, *args, **kwargs):
        self.instance.verified_at = timezone.now()
        return super(VerifyPhoneNumberForm, self).save(*args, **kwargs)


class NoFieldsPhoneNumberForm(BaseModelForm):
    class Meta:
        model = PhoneNumber
        fields = tuple()
