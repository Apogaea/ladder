import datetime

from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.utils import timezone
from django.conf import settings
from localflavor.us import models as us_models
from django.utils.functional import cached_property
from django.core.urlresolvers import reverse

from ladder.models import TimestampableModel

from accounts.models import User


def default_match_expiration():
    return timezone.now() + datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)


class MatchQuerySet(models.QuerySet):
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
            matches__ticket_request__is_cancelled=False,
            matches__ticket_request__is_terminated=False,
            matches__ticket_offer__is_cancelled=False,
            matches__ticket_offer__is_terminated=False,
        )

    def is_active(self):
        return self.exclude(
            Q(is_cancelled=True) | Q(is_terminated=True)
        ).exclude(
            matches__accepted_at__isnull=False,
            matches__is_terminated=False,
        ).exclude(
            matches__accepted_at__isnull=True,
            matches__created_at__gt=timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME),
            matches__is_terminated=False,
            matches__ticket_request__is_cancelled=False,
            matches__ticket_request__is_terminated=False,
            matches__ticket_offer__is_cancelled=False,
            matches__ticket_offer__is_terminated=False,
        )


class BaseMatchModel(TimestampableModel):
    is_cancelled = models.BooleanField(blank=True, default=False)
    is_terminated = models.BooleanField(blank=True, default=False)

    objects = MatchQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ('-created_at',)

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
            ticket_request__is_cancelled=False,
            ticket_request__is_terminated=False,
            ticket_offer__is_cancelled=False,
            ticket_offer__is_terminated=False,
            accepted_at__isnull=True,
            is_terminated=False,
            created_at__gt=timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME),
        ).exists()

    def get_status_display(self):
        if self.is_terminated:
            return u'Terminated'
        elif self.is_cancelled:
            return u'Cancelled'
        elif self.is_fulfilled:
            return u'Fulfilled'
        elif self.is_reserved:
            return u'Reserved'
        elif self.is_active:
            return u'Active'
        else:
            assert False, 'this should not be possible'

    def get_pending_match(self):
        return self.matches.is_awaiting_confirmation().first()


class TicketRequestQuerySet(MatchQuerySet):
    def is_active(self):
        return super(TicketRequestQuerySet, self).is_active().exclude(
            matches__accepted_at__isnull=True,
            matches__created_at__lt=timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME),
            matches__is_terminated=False,
            matches__ticket_request__is_cancelled=False,
            matches__ticket_request__is_terminated=False,
            matches__ticket_offer__is_cancelled=False,
            matches__ticket_offer__is_terminated=False,
        )


class TicketRequest(BaseMatchModel):
    user = models.ForeignKey(User, related_name='ticket_requests')
    message = models.TextField(max_length=1000)

    objects = TicketRequestQuerySet.as_manager()

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('request_detail', kwargs={'pk': self.pk})

    @cached_property
    def is_active(self):
        if self.is_cancelled or self.is_terminated:
            return False
        elif self.matches.is_awaiting_confirmation().exists():
            return False
        elif self.matches.is_accepted().exists():
            return False
        elif self.matches.is_expired().exists():
            return False
        return True


class TicketOffer(BaseMatchModel):
    user = models.ForeignKey(User, related_name='ticket_offers')

    is_automatch = models.BooleanField(blank=True, default=True)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('offer_detail', kwargs={'pk': self.pk})

    @cached_property
    def is_active(self):
        if self.is_cancelled or self.is_terminated:
            return False
        elif self.matches.is_awaiting_confirmation().exists():
            return False
        elif self.matches.is_accepted().exists():
            return False
        return True


class TicketMatchQuerySet(models.QuerySet):
    def is_accepted(self):
        return self.filter(
            accepted_at__isnull=False,
            is_terminated=False
        )

    def is_awaiting_confirmation(self):
        return self.filter(
            accepted_at__isnull=True,
            is_terminated=False,
            created_at__gt=timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME),
            ticket_request__is_cancelled=False,
            ticket_request__is_terminated=False,
            ticket_offer__is_cancelled=False,
            ticket_offer__is_terminated=False,
        )

    def is_expired(self):
        return self.filter(
            accepted_at__isnull=True,
            is_terminated=False,
            created_at__lte=timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME),
            ticket_request__is_cancelled=False,
            ticket_request__is_terminated=False,
            ticket_offer__is_cancelled=False,
            ticket_offer__is_terminated=False,
        )


class TicketMatch(TimestampableModel):
    ticket_request = models.ForeignKey('TicketRequest', related_name='matches')
    ticket_offer = models.ForeignKey('TicketOffer', related_name='matches')

    accepted_at = models.DateTimeField(null=True)

    is_terminated = models.BooleanField(default=False, blank=True)

    objects = TicketMatchQuerySet.as_manager()

    @cached_property
    def is_accepted(self):
        return self.accepted_at is not None and not self.is_terminated

    @cached_property
    def is_awaiting_confirmation(self):
        return all((
            self.accepted_at is None,
            self.is_terminated is False,
            self.created_at > timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME),
            self.ticket_request.is_cancelled is False,
            self.ticket_request.is_terminated is False,
            self.ticket_offer.is_cancelled is False,
            self.ticket_offer.is_terminated is False,
        ))

    @cached_property
    def is_expired(self):
        return all((
            self.accepted_at is None,
            self.is_terminated is False,
            self.created_at < timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME),
            self.ticket_request.is_cancelled is False,
            self.ticket_request.is_terminated is False,
            self.ticket_offer.is_cancelled is False,
            self.ticket_offer.is_terminated is False,
        ))

    @property
    def expires_at(self):
        return self.created_at + datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)

    def get_status_display(self):
        if self.is_accepted:
            return 'Completed'
        elif self.is_awaiting_confirmation:
            return 'Awaiting Confirmation'
        elif self.is_expired:
            return 'Expired'

    def get_absolute_url(self):
        return reverse('match_detail', kwargs={'pk': self.pk})


class LadderProfile(models.Model):
    user = models.OneToOneField('accounts.User', related_name='_profile')
    phone_number = us_models.PhoneNumberField("Phone Number", max_length=255,
                                              help_text=u"US Phone Number (XXX-XXX-XXXX)",
                                              unique=True)

    #
    #  Permission Shortcuts
    #
    @property
    def can_offer_ticket(self):
        if self.user.ticket_requests.is_active().exists():
            return False
        elif self.user.ticket_requests.is_reserved().exists():
            return False
        elif self.user.ticket_offers.is_active().count() + self.user.ticket_offers.is_reserved().count() > 4:
            return False
        return True

    @property
    def can_request_ticket(self):
        if self.user.ticket_requests.is_active().exists():
            return False
        elif self.user.ticket_requests.is_reserved().exists():
            return False
        elif self.user.ticket_offers.is_active().exists():
            return False
        elif self.user.ticket_offers.is_reserved().exists():
            return False
        return True


def create_ladder_profile(sender, instance, created, raw, **kwargs):
    if created and not raw:
        LadderProfile.objects.get_or_create(user=instance)

# Connect to the post_save signal of our `User` model to create a blank
# LadderProfile.
post_save.connect(create_ladder_profile, sender=User)
