import datetime

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.utils.functional import cached_property
from django.core.urlresolvers import reverse

from localflavor.us import models as us_models

from ladder.core.abstract_models import TimestampableModel


def default_match_expiration():
    return timezone.now() + datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)


class MatchQuerySet(models.QuerySet):
    def is_fulfilled(self):
        return self.filter(
            matches__accepted_at__isnull=False,
            matches__is_terminated=False,
        )

    def is_reserved(self):
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
        return self.exclude(
            matches__accepted_at__isnull=False,
            matches__is_terminated=False,
        ).filter(
            matches__accepted_at__isnull=True,
            matches__created_at__gt=cutoff,
            matches__is_terminated=False,
            matches__ticket_request__is_cancelled=False,
            matches__ticket_request__is_terminated=False,
            matches__ticket_offer__is_cancelled=False,
            matches__ticket_offer__is_terminated=False,
        )

    def is_active(self):
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
        return self.exclude(
            Q(is_cancelled=True) | Q(is_terminated=True)
        ).exclude(
            matches__accepted_at__isnull=False,
            matches__is_terminated=False,
        ).exclude(
            matches__accepted_at__isnull=True,
            matches__created_at__gt=cutoff,
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
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
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
            created_at__gt=cutoff,
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

    def get_accepted_match(self):
        return self.matches.is_accepted().first()


class TicketRequestQuerySet(MatchQuerySet):
    def is_active(self):
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
        return super(TicketRequestQuerySet, self).is_active().exclude(
            matches__accepted_at__isnull=True,
            matches__created_at__lt=cutoff,
            matches__is_terminated=False,
            matches__ticket_request__is_cancelled=False,
            matches__ticket_request__is_terminated=False,
            matches__ticket_offer__is_cancelled=False,
            matches__ticket_offer__is_terminated=False,
        )


class TicketRequest(BaseMatchModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ticket_requests')
    message = models.TextField(max_length=1000)

    objects = TicketRequestQuerySet.as_manager()

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('request-detail', kwargs={'pk': self.pk})

    @property
    def place_in_line(self):
        if not self.is_active:
            return None
        return TicketRequest.objects.filter(
            created_at__lt=self.created_at,
        ).is_active().count()

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ticket_offers')

    is_automatch = models.BooleanField(blank=True, default=True)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('offer-detail', kwargs={'pk': self.pk})

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
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
        return self.filter(
            accepted_at__isnull=True,
            is_terminated=False,
            created_at__gt=cutoff,
            ticket_request__is_cancelled=False,
            ticket_request__is_terminated=False,
            ticket_offer__is_cancelled=False,
            ticket_offer__is_terminated=False,
        )

    def is_expired(self):
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
        return self.filter(
            accepted_at__isnull=True,
            is_terminated=False,
            created_at__lte=cutoff,
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
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
        return all((
            self.accepted_at is None,
            self.is_terminated is False,
            self.created_at > cutoff,
            self.ticket_request.is_cancelled is False,
            self.ticket_request.is_terminated is False,
            self.ticket_offer.is_cancelled is False,
            self.ticket_offer.is_terminated is False,
        ))

    @cached_property
    def is_expired(self):
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
        return all((
            self.accepted_at is None,
            self.is_terminated is False,
            self.created_at < cutoff,
            self.ticket_request.is_cancelled is False,
            self.ticket_request.is_terminated is False,
            self.ticket_offer.is_cancelled is False,
            self.ticket_offer.is_terminated is False,
        ))

    @property
    def expires_at(self):
        return self.created_at + datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)

    def get_status_display(self):
        if self.is_terminated:
            return 'Terminated'
        elif self.ticket_request.is_terminated:
            return 'Ticket Request Terminated'
        elif self.ticket_request.is_cancelled:
            return 'Ticket Request Cancelled'
        elif self.ticket_offer.is_terminated:
            return 'Ticket Offer Terminated'
        elif self.ticket_offer.is_cancelled:
            return 'Ticket Offer Cancelled'
        elif self.is_accepted:
            return 'Accepted'
        elif self.is_awaiting_confirmation:
            return 'Awaiting Confirmation'
        elif self.is_expired:
            return 'Expired'

    def get_absolute_url(self):
        return reverse('match-detail', kwargs={'pk': self.pk})


class LadderProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='_profile')
    phone_number = us_models.PhoneNumberField("Phone Number", max_length=255,
                                              help_text=u"US Phone Number (XXX-XXX-XXXX)",
                                              unique=True)

    max_allowed_matches = models.PositiveIntegerField(blank=True, default=2)

    #
    #  Permission Shortcuts
    #
    @property
    def can_offer_ticket(self):
        if self.user.ticket_requests.is_active().exists():
            return False
        elif self.user.ticket_requests.is_reserved().exists():
            return False
        elif self.has_reached_max_allowed_matches:
            return False
        return True

    @property
    def has_reached_max_allowed_matches(self):
        active_offer_count = self.user.ticket_offers.is_active().count()
        reserved_offer_count = self.user.ticket_offers.is_reserved().count()
        fulfilled_offer_count = self.user.ticket_offers.is_fulfilled().count()

        total_matches = active_offer_count + reserved_offer_count + fulfilled_offer_count
        return total_matches >= self.max_allowed_matches

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
