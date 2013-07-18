from django.core.management.base import BaseCommand

from accounts.models import User

from exchange.management.commands.seed_requests import (
    get_user_kwargs, get_phone_number_kwargs,
)


class Command(BaseCommand):
    help = 'Creates ticket requests for testing'

    def handle(self, *args, **kwargs):
        for i in xrange(10):
            user = User.objects.create(
                display_name='User #{0}'.format(User.objects.count()),
                **get_user_kwargs()
            )
            user.ladder_profile.verified_phone_number = user.ladder_profile.phone_numbers.create(
                **get_phone_number_kwargs()
            )
            user.ticket_offers.create(is_automatch=bool(i % 2))
        self.stdout.write('Successfully created 10 ticket offers')
