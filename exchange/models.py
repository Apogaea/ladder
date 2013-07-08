import datetime
import hashlib
import time

from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.conf import settings
from django.db.models import F
from django.contrib.localflavor.us import models as us_models

from fusionbox import behaviors
from twilio.rest import TwilioRestClient

from accounts.models import User


twilio_client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

class TicketRequest(behaviors.Timestampable, behaviors.QuerySetManagerModel):
    user = models.ForeignKey(User, related_name='requests')
    message = models.TextField(max_length=1000)

    is_cancelled = models.BooleanField(blank=True, default=False)
    is_terminated = models.BooleanField(blank=True, default=False)

    class QuerySet(QuerySet):
        def is_fulfilled(self):
            pass

        def is_reserved(sefl):
            pass

        def is_active(self):
            pass

    class Meta:
        ordering = ('created_at',)

    def is_reserved(self):
        pass

    def is_fulfilled(self):
        pass

    def is_active(self):
        pass


class TicketOffer(behaviors.Timestampable, behaviors.QuerySetManagerModel):
    user = models.ForeignKey(User, related_name='listings')

    is_automatch = models.BooleanField(blank=True, default=True)
    is_cancelled = models.BooleanField(blank=True, default=False)
    is_terminated = models.BooleanField(blank=True, default=False)

    class QuerySet(QuerySet):
        def is_fulfilled(self):
            pass

        def is_reserved(sefl):
            pass

        def is_active(self):
            pass

    class Meta:
        ordering = ('created_at',)

    @models.permalink
    def get_absolute_url(self):
        return ('exchange.views.listing_detail', [], {'pk': self.pk})

    def is_reserved(self):
        pass

    def is_fulfilled(self):
        pass

    def is_active(self):
        pass


def default_match_expiration():
    return timezone.now() + datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)


class TicketMatch(behaviors.Timestampable, behaviors.QuerySetManagerModel):
    ticket_request = models.ForeignKey('TicketRequest', related_name='matches')
    ticket_offer = models.ForeignKey('TicketOffer', related_name='matches')

    expires_at = models.DateTimeField(default=default_match_expiration)
    is_accepted = models.BooleanField(default=False, blank=True)

    is_terminated = models.BooleanField(default=False, blank=True)


class LadderProfile(behaviors.QuerySetManagerModel):
    phone_number = us_models.PhoneNumberField("Phone Number", max_length=255,
            help_text=u"US Phone Number (XXX-XXX-XXXX)")
    verified_at = models.DateTimeField(blank=True, null=True)

    #|
    #|  Permission Shortcuts
    #|
    @property
    def can_send_code(self):
        if not self.codes.exists():
            return False
        latest = self.codes.latest('last_sent_at')
        return latest.can_send

    @property
    def can_list_ticket(self):
        if self.verified_at is None:
            return False
        if self.requests.is_active().exists():
            return False
        return True

    @property
    def can_request_ticket(self):
        if self.verified_at is None:
            return False
        if self.listings.is_active().exists():
            return False
        return True


class PhoneNumber(behaviors.QuerySetManagerModel, behaviors.Timestampable):
    user = models.ForeignKey('LadderProfile', related_name='codes')
    phone_number = us_models.PhoneNumberField("Phone Number", max_length=255, blank=True)
    confirmation_code = models.CharField(max_length=255, blank=True, editable=False)

    attempts = models.PositiveIntegerField(default=0, blank=True)
    last_sent_at = models.DateTimeField(blank=True, null=True, editable=False)

    class Meta:
        ordering = ('-last_sent_at',)
        get_latest_by = 'created_at'

    class QuerySet(QuerySet):
        def active(self):
            expire_cutoff = timezone.now() - datetime.timedelta(minutes=settings.TWILIO_CODE_EXPIRE_MINUTES)
            return self.filter(
                    last_sent_at__gte=expire_cutoff,
                    attempts__lte=settings.TWILIO_CODE_MAX_ATTEMPTS,
                    phone_number=F('user__phone_number'),
                    )

        # TODO: get this code out of the model.
        def validate(self, code):
            assert code
            if self.active().filter(code=code):
                return True
            else:
                return False

    def save(self, *args, **kwargs):
        if not self.id and not self.code:
            self.phone_number = self.user.phone_number
            self.set_code()
        super(PhoneNumber, self).save(*args, **kwargs)

    def set_code(self):
        hasher = hashlib.sha256()
        # TODO make this more secure
        hash_string = '{user.pk}:{user.created_at}:{self.pk}:{self.created_at}'.format(
                self=self,
                user=self.user,
                )
        hasher.update(hash_string)
        code = hasher.hexdigest().__hash__() % 1000000
        self.code = '{0:06d}'.format(code)

    def send(self):
        twilio_client.sms.messages.create(
            to=self.user.phone_number,
            from_='+12404282876',
            body='Apogaea Ladder Verification Code: "{code}"'.format(code=self.code),
        )
        self.last_sent_at = timezone.now()
        self.attempts += 1
        self.save()

    @property
    def can_send(self):
        # Sanity check
        if not self.phone_number == self.user.phone_number:
            assert False
        if self.sent_at:
            resend_time = self.last_sent_at + datetime.timedelta(minutes=settings.TWILIO_RESEND_MINUTES)
            return timezone.now() < resend_time
        else:
            return True
