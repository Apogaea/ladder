import pytest

from django_webtest import (
    WebTest as BaseWebTest,
    DjangoTestApp as BaseDjangoTestApp,
)


@pytest.fixture()  # NOQA
def factories(db):
    import factory
    #from tests.accounts.factories import (  # NOQA
    #    UserFactory,
    #)

    def is_factory(obj):
        if not isinstance(obj, type):
            return False
        return issubclass(obj, factory.DjangoModelFactory)

    dict_ = {k: v for k, v in locals().items() if is_factory(v)}

    return type(
        'fixtures',
        (object,),
        dict_,
    )


@pytest.fixture()  # NOQA
def models(db):
    from django.apps import apps

    dict_ = {M._meta.object_name: M for M in apps.get_models()}

    return type(
        'models',
        (object,),
        dict_,
    )


class DjangoTestApp(BaseDjangoTestApp):
    @property
    def user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_id = self.session.get('_auth_user_id')
        if user_id:
            return User.objects.get(pk=user_id)
        else:
            return None


class WebTest(BaseWebTest):
    app_class = DjangoTestApp

    def authenticate(self, user):
        self.app.get('/', user=user)

    def unauthenticate(self):
        self.app.get('/', user=None)


@pytest.fixture()  # NOQA
def webtest_client(db):
    web_test = WebTest(methodName='__call__')
    web_test()
    return web_test.app


@pytest.fixture()
def user_webtest_client(webtest_client, user):
    web_test = WebTest(methodName='__call__')
    web_test()
    web_test.authenticate(user)
    return web_test.app


@pytest.fixture()  # NOQA
def User(db):
    """
    A slightly more intuitively named
    `pytest_django.fixtures.django_user_model`
    """
    from django.contrib.auth import get_user_model
    return get_user_model()


@pytest.fixture()
def admin_user(User):
    try:
        return User.objects.get(email='admin@example.com')
    except User.DoesNotExist:
        return User.objects.create_superuser(
            display_name='admin',
            email='admin@example.com',
            password='password',
        )


@pytest.fixture()
def user(User):
    try:
        return User.objects.get(
            email='test@example.com',
        )
    except User.DoesNotExist:
        return User.objects.create_user(
            display_name='Test User',
            email='test@example.com',
            password='password',
        )
