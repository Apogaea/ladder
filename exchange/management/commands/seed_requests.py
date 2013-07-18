from uuid import uuid4

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User


def get_user_kwargs():
    return {
        'email': str(uuid4()) + '@example.com',
    }


def get_phone_number_kwargs(is_verified=False):
    number = hash(str(uuid4())) % 10000000000
    kwargs = {
        'phone_number': number,
    }
    if is_verified:
        kwargs['verified_at'] = timezone.now()
    return kwargs


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
            user.ticket_requests.create(message='Generated ticket request.')
        self.stdout.write('Successfully created 10 ticket requests')
