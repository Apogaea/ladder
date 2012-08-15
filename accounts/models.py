import hashlib
import time

from django.db import models
from django.contrib.auth.models import User as DjangoUser, UserManager as DjangoUserManager
from django.contrib.localflavor.us import models as us_models

from fusionbox import behaviors
from fusionbox.db.models import QuerySetManager


class UserManager(QuerySetManager, DjangoUserManager):
    pass


class User(behaviors.QuerySetManagerModel, DjangoUser):
    display_name = models.CharField(max_length=255, blank=True)

    phone_number = us_models.PhoneNumberField(max_length=255)
    is_verified = models.BooleanField(blank=True, default=False)
    verified_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    def __unicode__(self):
        if self.display_name:
            return self.display_name
        elif self.first_name or self.last_name:
            return '{0} {1}'.format(self.first_name, self.last_name).strip()
        else:
            super(User, self).__unicode__()


class PhoneVerification(behaviors.Timestampable):
    user = models.ForeignKey(User, related_name='verifications')
    code = models.CharField(max_length=255, blank=True, editable=False)

    sent_at = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.id and not self.code:
            self.set_code()
        super(PhoneVerification, self).save(*args, **kwargs)

    def set_code(self):
        hasher = hashlib.md5()
        # TODO make this more secure
        hash_string = '{user.user_ptr_id}:{user.id}:{timestamp}'.format(
                user=self.user,
                timestamp=time.time(),
                )
        hasher.update(hash_string)
        code = hasher.hexdigest().__hash__() % 1000000
        self.code = '{0:06d}'.format(code)

    def send(self):
        from twilio.rest import TwilioRestClient
        from django.conf import settings

        client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.sms.messages.create(
                to=self.user.phone_number,
                from_='+12404282876',
                body='Apogaea Ladder Verification Code: "{code}"'.format(code=self.code),
                )
