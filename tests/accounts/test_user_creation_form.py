from ladder.apps.accounts.forms import UserCreationForm

from ladder.apps.accounts.utils import generate_phone_number_code


def test_with_sms_code_raw():
    phone_number = '555-444-3210'
    code = generate_phone_number_code(phone_number)
    data = {
        'sms_code': code,
        'display_name': 'Test Name',
        'password': 'password',
    }
    form = UserCreationForm(phone_number=phone_number, data=data)
    assert form.is_valid(), form.errors


def test_with_sms_code_with_spaces():
    phone_number = '555-444-3210'
    code = generate_phone_number_code(phone_number)
    code_with_spaces = "{0} {1}".format(code[:3], code[3:])
    data = {
        'sms_code': code_with_spaces,
        'display_name': 'Test Name',
        'password': 'password',
    }
    form = UserCreationForm(phone_number=phone_number, data=data)
    assert form.is_valid(), form.errors
