from celery import task

from twilio.rest import TwilioRestClient

from django.conf import settings


@task(ignore_result=True)
def send_sms(**kwargs):
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.sms.messages.create(**kwargs)
