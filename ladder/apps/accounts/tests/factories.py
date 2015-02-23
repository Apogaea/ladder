from django.db.models.signals import post_save

import factory

from accounts.models import User
from exchange.models import create_ladder_profile


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    is_active = True
    email = factory.Sequence(lambda i: 'test-{0}@example.com'.format(i))

    password = factory.PostGenerationMethodCall('set_password', 'secret')

    @classmethod
    def _generate(cls, create, attrs):
        """Override the default _generate() to disable the post-save signal."""

        # Note: If the signal was defined with a dispatch_uid, include that in both calls.
        post_save.disconnect(create_ladder_profile, User)
        user = super(UserFactory, cls)._generate(create, attrs)
        post_save.connect(create_ladder_profile, User)
        return user


class SuperUserFactory(UserFactory):
    is_superuser = True
    is_staff = True


class UserWithProfileFactory(UserFactory):
    _profile = factory.RelatedFactory('exchange.tests.factories.LadderProfileFactory', 'user')


class SuperUserWithProfileFactory(SuperUserFactory):
    _profile = factory.RelatedFactory('exchange.tests.factories.LadderProfileFactory', 'user')
