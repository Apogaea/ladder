import datetime

from django.utils import timezone
from django.conf import settings

import factory

from exchange.models import (
    LadderProfile, TicketRequest, TicketOffer, TicketMatch,
)


class LadderProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = LadderProfile

    user = factory.SubFactory('accounts.tests.factories.UserFactory')
    phone_number = factory.Sequence(lambda i: '555-555-{0}'.format(str(i).zfill(4)))


class TicketRequestFactory(factory.DjangoModelFactory):
    FACTORY_FOR = TicketRequest

    user = factory.SubFactory('accounts.tests.factories.UserFactory')
    message = 'I would like a ticket'


class TicketOfferFactory(factory.DjangoModelFactory):
    FACTORY_FOR = TicketOffer

    user = factory.SubFactory('accounts.tests.factories.UserFactory')


class TicketMatchFactory(factory.DjangoModelFactory):
    FACTORY_FOR = TicketMatch

    ticket_request = factory.SubFactory('exchange.tests.factories.TicketRequestFactory')
    ticket_offer = factory.SubFactory('exchange.tests.factories.TicketOfferFactory')


class AcceptedTicketMatchFactory(TicketMatchFactory):
    accepted_at = factory.LazyAttribute(lambda o: timezone.now())


class ExpiredTicketMatchFactory(TicketMatchFactory):
    created_at = factory.LazyAttribute(
        lambda o: timezone.now() - datetime.timedelta(seconds=settings.DEFAULT_ACCEPT_TIME + 1)
    )
