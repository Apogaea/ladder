from django.db import models
from django.db.models.query import QuerySet

from fusionbox import behaviors

from accounts.models import User


class TicketRequest(behaviors.Timestampable, behaviors.QuerySetManagerModel):
    user = models.ForeignKey(User, related_name='requests')

    class QuerySet(QuerySet):
        def active(self):
            # TODO - make this do something
            return self


class TicketOffer(behaviors.Timestampable, behaviors.QuerySetManagerModel):
    user = models.ForeignKey(User, related_name='offers')

    TYPE_CHOICES = (
            ('direct', 'Manual Distribution'),
            ('automatic', 'Automatic Distribution'),
            )
    type = models.CharField('Offer Type', choices=TYPE_CHOICES, 
            max_length=255, default=None)

    class QuerySet(QuerySet):
        def active(self):
            # TODO - make this do something
            return self
