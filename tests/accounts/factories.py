from django.utils import timezone
from django.db.models.signals import post_save

import factory

from ladder.apps.accounts.models import User
from ladder.apps.exchange.receivers import create_ladder_profile


class UserFactory(factory.DjangoModelFactory):
    is_active = True
    display_name = factory.Sequence(lambda i: 'test-user-{0}'.format(i))
    email = factory.Sequence(lambda i: 'test-{0}@example.com'.format(i))

    password = factory.PostGenerationMethodCall('set_password', 'secret')

    last_login = factory.LazyAttribute(lambda u: timezone.now())

    @classmethod
    def _generate(cls, create, attrs):
        """Override the default _generate() to disable the post-save signal."""

        # Note: If the signal was defined with a dispatch_uid, include that in both calls.
        post_save.disconnect(create_ladder_profile, User)
        user = super(UserFactory, cls)._generate(create, attrs)
        post_save.connect(create_ladder_profile, User)
        return user

    class Meta:
        model = User
        django_get_or_create = ('email',)


class SuperUserFactory(UserFactory):
    is_superuser = True
    is_staff = True


class UserWithProfileFactory(UserFactory):
    _profile = factory.RelatedFactory('tests.exchange.factories.LadderProfileFactory', 'user')


class SuperUserWithProfileFactory(SuperUserFactory):
    _profile = factory.RelatedFactory('tests.exchange.factories.LadderProfileFactory', 'user')
