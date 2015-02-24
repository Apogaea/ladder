import datetime

from django.utils import timezone
from django.conf import settings

import factory

from ladder.apps.exchange.models import (
    LadderProfile,
    TicketRequest,
    TicketOffer,
    TicketMatch,
)


class LadderProfileFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('tests.accounts.factories.UserWithProfileFactory')
    phone_number = factory.Sequence(lambda i: '555-555-{0}'.format(str(i).zfill(4)))

    class Meta:
        model = LadderProfile


class TicketRequestFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('tests.accounts.factories.UserWithProfileFactory')
    message = 'I would like a ticket'

    class Meta:
        model = TicketRequest


class TicketOfferFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('tests.accounts.factories.UserWithProfileFactory')

    class Meta:
        model = TicketOffer


class TicketMatchFactory(factory.DjangoModelFactory):
    ticket_request = factory.SubFactory('tests.exchange.factories.TicketRequestFactory')
    ticket_offer = factory.SubFactory('tests.exchange.factories.TicketOfferFactory')

    class Meta:
        model = TicketMatch


class AcceptedTicketMatchFactory(TicketMatchFactory):
    accepted_at = factory.LazyAttribute(lambda o: timezone.now())


class ExpiredTicketMatchFactory(TicketMatchFactory):
    created_at = factory.LazyAttribute(
        lambda o: timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME + 1)
    )
