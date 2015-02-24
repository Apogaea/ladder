from django.utils import timezone

import factory

from ladder.apps.accounts.models import User


class UserFactory(factory.DjangoModelFactory):
    is_active = True
    display_name = factory.Sequence(lambda i: 'test-user-{0}'.format(i))
    email = factory.Sequence(lambda i: 'test-{0}@example.com'.format(i))

    password = factory.PostGenerationMethodCall('set_password', 'secret')

    last_login = factory.LazyAttribute(lambda u: timezone.now())

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
