from django.db import models, IntegrityError
from django.db.models.query import QuerySet

from fusionbox import behaviors

from accounts.models import User


class TicketRequest(behaviors.Timestampable, behaviors.QuerySetManagerModel):
    user = models.ForeignKey(User, related_name='requests')
    message = models.TextField(max_length=1000)

    is_cancelled = models.BooleanField(blank=True, default=False)

    class QuerySet(QuerySet):
        def active(self):
            return self.filter(is_cancelled=False, listing__isnull=True)

    class Meta:
        ordering = ('created_at',)

    @property
    def is_fulfilled(self):
        try:
            return bool(self.listing)
        except TicketListing.DoesNotExist:
            return False


class TicketListing(behaviors.Timestampable, behaviors.QuerySetManagerModel):
    user = models.ForeignKey(User, related_name='listings')

    TYPE_CHOICES = (
            ('direct', 'Manual Distribution'),
            ('automatic', 'Automatic Distribution'),
            )
    type = models.CharField('Listing Type', choices=TYPE_CHOICES,
            max_length=255, default=None, db_index=True)
    is_cancelled = models.BooleanField(blank=True, default=False)
    request = models.OneToOneField(TicketRequest, related_name='listing', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.request_id and self.is_cancelled:
            raise IntegrityError('A TicketListing may not be cancelled when linked to a TicketRequest')
        return super(TicketListing, self).save(*args, **kwargs)

    class QuerySet(QuerySet):
        def active(self):
            return self.filter(is_cancelled=False, request__isnull=True)

    class Meta:
        ordering = ('created_at',)

    @models.permalink
    def get_absolute_url(self):
        return ('exchange.views.listing_detail', [], {'pk': self.pk})
