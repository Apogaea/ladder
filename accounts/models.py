import hashlib
import time
import datetime

from django.db import models
from django.db.models import F
from django.db.models.query import QuerySet
from django.contrib.auth.models import User as DjangoUser, UserManager as DjangoUserManager
from django.contrib.localflavor.us import models as us_models
from django.conf import settings

from twilio.rest import TwilioRestClient

from fusionbox import behaviors
from fusionbox.db.models import QuerySetManager

from ladder.util import now


class UserManager(QuerySetManager, DjangoUserManager):
    pass


class User(behaviors.QuerySetManagerModel, DjangoUser):
    display_name = models.CharField(max_length=255, blank=True,
            help_text=u"What your name will show up as on the site")

    phone_number = us_models.PhoneNumberField("Phone Number", max_length=255,
            help_text=u"US Phone Number (XXX-XXX-XXXX)")
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

    def validate(self, code):
        assert code
        if self.codes.active().filter(code=code):
            self.is_verified = True
            self.verified_at = now()
            self.save()
            return True
        else:
            self.codes.update(attempts=F('attempts') + 1)
            return False

    #|
    #|  Permission Shortcuts
    #|
    @property
    def can_send_code(self):
        if not self.codes.exists():
            return False
        latest = self.codes.latest('sent_at')
        return latest.can_send

    @property
    def can_offer_ticket(self):
        if not self.is_verified:
            return False
        if self.requests.active().exists():
            return False
        return True

    @property
    def can_request_ticket(self):
        if not self.is_verified:
            return False
        if self.offers.active().exists():
            return False
        return True


class PhoneVerification(behaviors.QuerySetManagerModel, behaviors.Timestampable):
    user = models.ForeignKey(User, related_name='codes')
    phone_number = us_models.PhoneNumberField("Phone Number", max_length=255, blank=True)
    code = models.CharField(max_length=255, blank=True, editable=False)

    attempts = models.PositiveIntegerField(default=0, blank=True)
    sent_at = models.DateTimeField(blank=True, null=True, editable=False)

    class Meta:
        ordering = ('-sent_at',)
        get_latest_by = 'created_at'

    class QuerySet(QuerySet):
        def active(self):
            expire_cutoff = now() - datetime.timedelta(minutes=settings.TWILIO_CODE_EXPIRE_MINUTES)
            return self.filter(
                    sent_at__gte=expire_cutoff,
                    attempts__lte=settings.TWILIO_CODE_MAX_ATTEMPTS,
                    phone_number=F('user__phone_number'),
                    )

    def save(self, *args, **kwargs):
        if not self.id and not self.code:
            self.phone_number = self.user.phone_number
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
        client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.sms.messages.create(
                to=self.user.phone_number,
                from_='+12404282876',
                body='Apogaea Ladder Verification Code: "{code}"'.format(code=self.code),
                )
        self.sent_at = datetime.datetime.now()
        self.save()

    @property
    def can_send(self):
        # Sanity check
        if not self.phone_number == self.user.phone_number:
            assert False
        if self.sent_at:
            resend_time = self.sent_at + datetime.timedelta(minutes=settings.TWILIO_RESEND_MINUTES)
            return datetime.datetime.now() < resend_time
        else:
            return True
