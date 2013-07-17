import datetime
import hashlib

from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.db.models.query import QuerySet
from django.utils import timezone
from django.conf import settings
from django.db.models import F
from django_localflavor_us import models as us_models
from django.utils.functional import cached_property, SimpleLazyObject
from django.core.urlresolvers import reverse
from django.utils import crypto

from fusionbox import behaviors

from twilio.rest import TwilioRestClient

from accounts.models import User

twilio_client = SimpleLazyObject(lambda: TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN))


def default_match_expiration():
    return timezone.now() + datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)


class BaseMatchModel(behaviors.Timestampable, behaviors.QuerySetManagerModel):
    is_cancelled = models.BooleanField(blank=True, default=False)
    is_terminated = models.BooleanField(blank=True, default=False)

    class Meta:
        abstract = True

    class QuerySet(QuerySet):
        def is_fulfilled(self):
            return self.filter(
                matches__accepted_at__isnull=False,
                matches__is_terminated=False,
            )

        def is_reserved(self):
            return self.exclude(
                matches__accepted_at__isnull=False,
                matches__is_terminated=False,
            ).filter(
                matches__accepted_at__isnull=True,
                matches__created_at__gt=timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME),
                matches__is_terminated=False,
            )

        def is_active(self):
            return self.exclude(
                Q(is_cancelled=True) | Q(is_terminated=True)
            ).exclude(
                matches__accepted_at__isnull=True,
                matches__created_at__gt=timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME),
                matches__is_terminated=False,
            ).exclude(
                matches__accepted_at__isnull=False,
                matches__is_terminated=False,
            )

    @cached_property
    def is_fulfilled(self):
        return self.matches.filter(
            accepted_at__isnull=False,
            is_terminated=False,
        ).exists()

    @cached_property
    def is_reserved(self):
        return self.matches.exclude(
            accepted_at__isnull=False,
            is_terminated=False,
        ).filter(
            accepted_at__isnull=True,
            is_terminated=False,
            created_at__gt=timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME),
        ).exists()

    @cached_property
    def is_active(self):
        if self.is_cancelled or self.is_terminated:
            return False
        return not self.matches.filter(
            Q(
                accepted_at__isnull=False,
                is_terminated=False,
            ) | Q(
                accepted_at__isnull=True,
                is_terminated=False,
                created_at__gt=timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME),
            )
        ).exists()


class TicketRequest(BaseMatchModel):
    user = models.ForeignKey(User, related_name='ticket_requests')
    message = models.TextField(max_length=1000)

    class Meta:
        ordering = ('created_at',)

    def get_absolute_url(self):
        return reverse('exchange.views.request_detail', kwargs={'pk': self.pk})


class TicketOffer(BaseMatchModel):
    user = models.ForeignKey(User, related_name='ticket_offers')

    is_automatch = models.BooleanField(blank=True, default=True)

    class Meta:
        ordering = ('created_at',)

    def get_absolute_url(self):
        return reverse('exchange.views.offer_detail', kwargs={'pk': self.pk})


class TicketMatch(behaviors.Timestampable, behaviors.QuerySetManagerModel):
    ticket_request = models.ForeignKey('TicketRequest', related_name='matches')
    ticket_offer = models.ForeignKey('TicketOffer', related_name='matches')

    accepted_at = models.DateTimeField(null=True)

    is_terminated = models.BooleanField(default=False, blank=True)

    def get_absolute_url(self):
        return reverse('exchange.views.match_detail', kwargs={'pk': self.pk})


class LadderProfile(behaviors.QuerySetManagerModel):
    user = models.OneToOneField('accounts.User', related_name='ladder_profile')
    verified_phone_number = models.ForeignKey('exchange.PhoneNumber', null=True, editable=False)

    class QuerySet(QuerySet):
        def is_verified(self):
            return self.filter(verified_phone_number__isnull=False)

    @cached_property
    def is_verified(self):
        return not self.verified_phone_number is None

    #|
    #|  Permission Shortcuts
    #|
    @property
    def can_offer_ticket(self):
        if self.verified_at is None:
            return False
        elif self.ticket_requests.is_active().exists():
            return False
        elif self.ticket_requests.is_reserved().exists():
            return False
        return True

    @property
    def can_request_ticket(self):
        if self.verified_at is None:
            return False
        elif self.ticket_requests.is_active().exists():
            return False
        elif self.ticket_requests.is_reserved().exists():
            return False
        return True


def create_ladder_profile(sender, instance, created, raw, **kwargs):
    if created and not raw:
        LadderProfile.objects.get_or_create(user=instance)

# Connect to the post_save signal of our `User` model to create a blank
# LadderProfile.
post_save.connect(create_ladder_profile, sender=User)


def get_a_verification_code():
    """
    Uses `get_random_string` from `django.utils.crypto` to generate a
    random string of characters which are then converted to a 6-digit
    numeric code padded with zeros.
    """
    random_string = crypto.get_random_string(50, 'abcdefghijklmnopqrstuvwxyz0123456789')
    code = hash(random_string) % 1000000
    return '{0:06d}'.format(code)


class PhoneNumber(behaviors.QuerySetManagerModel, behaviors.Timestampable):
    profile = models.ForeignKey('LadderProfile', related_name='phone_numbers')
    phone_number = us_models.PhoneNumberField("Phone Number", max_length=255,
                                              help_text=u"US Phone Number (XXX-XXX-XXXX)")
    verified_at = models.DateTimeField(null=True, editable=False)
    confirmation_code = models.CharField(max_length=255, blank=True,
                                         editable=False,
                                         default=get_a_verification_code)

    attempts = models.PositiveIntegerField(default=0, blank=True)
    last_sent_at = models.DateTimeField(blank=True, null=True, editable=False)

    class Meta:
        ordering = ('-last_sent_at',)
        get_latest_by = 'created_at'

    class QuerySet(QuerySet):
        def is_verified(self):
            return self.filter(verified_at__isnull=False)

        def is_verifiable(self):
            return self.filter(
                verified_at__isnull=True,
                last_sent_at__gt=timezone.now() - datetime.timedelta(minutes=settings.TWILIO_CODE_EXPIRE_MINUTES),
                attempts__lt=settings.TWILIO_CODE_MAX_ATTEMPTS,
            )

    def __unicode__(self):
        return self.phone_number

    @property
    def is_verified(self):
        return self.verified_at is not None

    @property
    def is_verifiable(self):
        if self.is_verified:
            return False
        if self.attempts >= settings.TWILIO_CODE_MAX_ATTEMPTS:
            return False
        return True

    def send_sms(self):
        twilio_client.sms.messages.create(
            to=self.phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            body='Apogaea Ladder Verification Code: "{code}"'.format(code=self.confirmation_code),
        )
        self.last_sent_at = timezone.now()
        self.attempts += 1
        self.save()

    @property
    def can_send(self):
        if not self.is_verifiable:
            return False
        if self.last_sent_at:
            resend_time = self.last_sent_at + datetime.timedelta(minutes=settings.TWILIO_RESEND_MINUTES)
            return timezone.now() > resend_time
        else:
            return True
