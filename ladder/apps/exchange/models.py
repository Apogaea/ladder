from __future__ import unicode_literals

import datetime
import logging

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.template.defaultfilters import truncatewords

from localflavor.us import models as us_models

from ladder.core.abstract_models import TimestampableModel


logger = logging.getLogger(__file__)


def default_match_expiration():
    return timezone.now() + datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)


class MatchQuerySet(models.QuerySet):
    def is_fulfilled(self):
        return self.filter(
            matches__accepted_at__isnull=False,
        )

    def is_reserved(self):
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
        return self.exclude(
            matches__accepted_at__isnull=False,
        ).filter(
            matches__accepted_at__isnull=True,
            matches__created_at__gt=cutoff,
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
        ).exclude(
            matches__accepted_at__isnull=True,
            matches__created_at__gt=cutoff,
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

    @property
    def is_fulfilled(self):
        return self.matches.filter(
            accepted_at__isnull=False,
            ticket_request__is_terminated=False,
            ticket_offer__is_terminated=False,
        ).exists()

    @property
    def is_reserved(self):
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
        return self.matches.exclude(
            accepted_at__isnull=False,
        ).filter(
            ticket_request__is_cancelled=False,
            ticket_request__is_terminated=False,
            ticket_offer__is_cancelled=False,
            ticket_offer__is_terminated=False,
            accepted_at__isnull=True,
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
            return u'Awaiting Confirmation'
        elif self.is_active:
            return u'Active'
        else:
            logger.error("Unknown status for %s:%s", self._meta.verbose_name, self.pk)
            return u'Unknown'

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
            matches__ticket_request__is_cancelled=False,
            matches__ticket_request__is_terminated=False,
            matches__ticket_offer__is_cancelled=False,
            matches__ticket_offer__is_terminated=False,
        )


class TicketRequest(BaseMatchModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ticket_requests')
    message = models.TextField(max_length=200)

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

    @property
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


@python_2_unicode_compatible
class BaseHistoryModel(TimestampableModel):
    """
    - Creation.
    - Cancelation
    - Termination
    - Match Found
    - Match Confirmed
    - Match Expired  (no event to tie to...)
    """
    message = models.CharField(max_length=255)

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    def __str__(self):
        return truncatewords(self.message, 10)


class TicketRequestHistory(BaseHistoryModel):
    ticket_request = models.ForeignKey('TicketRequest', related_name='history')


class TicketOffer(BaseMatchModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ticket_offers')
    ticket_code = models.CharField(
        max_length=20,
        help_text=(
            "The TicketFly confirmation code that was given to you when you "
            "purchased your ticket"
        )
    )

    is_automatch = models.BooleanField(blank=True, default=True)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('offer-detail', kwargs={'pk': self.pk})

    @property
    def is_active(self):
        if self.is_cancelled or self.is_terminated:
            return False
        elif self.matches.is_awaiting_confirmation().exists():
            return False
        elif self.matches.is_accepted().exists():
            return False
        return True


class TicketOfferHistory(BaseHistoryModel):
    ticket_offer = models.ForeignKey('TicketOffer', related_name='history')


class TicketMatchQuerySet(models.QuerySet):
    def is_accepted(self):
        return self.filter(
            accepted_at__isnull=False,
            ticket_request__is_terminated=False,
            ticket_offer__is_terminated=False,
        )

    def is_awaiting_confirmation(self):
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
        return self.filter(
            accepted_at__isnull=True,
            created_at__gt=cutoff,
            ticket_request__is_cancelled=False,
            ticket_request__is_terminated=False,
            ticket_offer__is_cancelled=False,
            ticket_offer__is_terminated=False,
        )

    def is_terminated(self):
        return self.filter(
            Q(ticket_request__is_terminated=True) | Q(ticket_offer__is_terminated=True)
        )

    def is_cancelled(self):
        return self.filter(
            Q(ticket_request__is_cancelled=True) | Q(ticket_offer__is_cancelled=True)
        )

    def is_expired(self):
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
        return self.filter(
            accepted_at__isnull=True,
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

    objects = TicketMatchQuerySet.as_manager()

    @property
    def is_accepted(self):
        return self.accepted_at is not None and not self.is_terminated

    @property
    def is_terminated(self):
        return self.ticket_request.is_terminated or self.ticket_offer.is_terminated

    @property
    def is_cancelled(self):
        return self.ticket_request.is_cancelled or self.ticket_offer.is_cancelled

    @property
    def is_awaiting_confirmation(self):
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
        return all((
            self.accepted_at is None,
            self.is_terminated is False,
            self.created_at > cutoff,
            self.ticket_request.is_cancelled is False,
            self.ticket_offer.is_cancelled is False,
        ))

    @property
    def is_expired(self):
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)
        return all((
            self.accepted_at is None,
            self.is_terminated is False,
            self.created_at < cutoff,
            self.ticket_request.is_cancelled is False,
            self.ticket_offer.is_cancelled is False,
        ))

    @property
    def expires_at(self):
        return self.created_at + datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME)

    def get_status_display(self):
        if self.is_terminated:
            if self.ticket_request.is_terminated and self.ticket_offer.is_terminated:
                return 'Both Request and Offer Terminated'
            elif self.ticket_request.is_terminated:
                return 'Ticket Request Terminated'
            elif self.ticket_offer.is_terminated:
                return 'Ticket Offer Terminated'
            else:
                logger.error("Unknown status for %s:%s", self._meta.verbose_name, self.pk)
                return u'Unknown'
        elif self.is_cancelled:
            if self.ticket_request.is_cancelled and self.ticket_offer.is_cancelled:
                return 'Both Request and Offer Cancelled'
            elif self.ticket_request.is_cancelled:
                return 'Ticket Request Cancelled'
            elif self.ticket_offer.is_cancelled:
                return 'Ticket Offer Cancelled'
            else:
                logger.error("Unknown status for %s:%s", self._meta.verbose_name, self.pk)
                return u'Unknown'
        elif self.is_accepted:
            return 'Accepted'
        elif self.is_awaiting_confirmation:
            return 'Awaiting Confirmation'
        elif self.is_expired:
            return 'Expired'
        else:
            logger.error("Unknown status for %s:%s", self._meta.verbose_name, self.pk)
            return u'Unknown'

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
