import datetime
import logging

from django.core import signing
from django.core.urlresolvers import reverse
from django.conf import settings

from twilio.rest import TwilioRestClient

logger = logging.getLogger(__name__)

twilio_client = TwilioRestClient(
    settings.TWILIO_ACCOUNT_SID,
    settings.TWILIO_AUTH_TOKEN,
)


REGISTRATION_SALT = 'ladder:registration'
REGISTRATION_TOKEN_MAX_AGE = 60 * 60 * 24 * 2  # 2 days


def generate_registration_token(email, phone_number):
    return signing.dumps((email, phone_number), salt=REGISTRATION_SALT)


def reverse_registration_url(email, phone_number):
    token = generate_registration_token(email, phone_number)
    return reverse('register-confirm', kwargs={'token': token})


def unsign_registration_token(token):
    return signing.loads(
        token, salt=REGISTRATION_SALT, max_age=REGISTRATION_TOKEN_MAX_AGE,
    )


def send_twilio_sms(phone_number, message):
    resp = twilio_client.sms.messages.create(
        to=phone_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=message,
    )
    logger.info('SMS: %s:"%s"', phone_number, message)
    return resp


PHONE_NUMBER_VERIFICATION_SALT = 'ladder:verify-phone-number'


def generate_phone_number_code(phone_number):
    signer = signing.Signer(salt=PHONE_NUMBER_VERIFICATION_SALT)
    signature = signer.sign("{phone_number}:{timestamp}".format(
        phone_number=phone_number,
        timestamp=datetime.datetime.now().strftime('%Y:%m:%d-%H'),
    ))
    code = hash(signature) % 1000000
    return str(code).zfill(6)


def send_phone_number_verification_sms(phone_number):
    code = generate_phone_number_code(phone_number)
    message = 'Apogaea Ladder Verification Code: {0} {1}'.format(
        code[:3], code[3:],
    )
    logger.info(message)
    return send_twilio_sms(phone_number, message)
