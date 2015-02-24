from django.core.urlresolvers import reverse

from rest_framework import status



def test_page_with_anonymous_user(factories, client):
    url = reverse('admin:login')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'form' in response.context


def test_page_with_authenticated_regular_user(factories, client):
    url = reverse('admin:login')
    user = factories.UserFactory(password='secret')
    assert client.login(username=user.email, password='secret')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'form' in response.context


def test_page_with_authenticated_admin(factories, client):
    url = reverse('admin:login')
    user = factories.SuperUserFactory(password='secret')

    assert client.login(username=user.email, password='secret')

    response = client.get(url)
    assert response.get('location', '').endswith(reverse('admin:index'))


def test_authentication_by_superuser(client, factories):
    url = reverse('admin:login')
    user = factories.SuperUserFactory(password='secret')
    response = client.post(url, {
        'username': user.email,
        'password': 'secret',
    })
    assert response.get('location', '').endswith(reverse('admin:index'))


def test_authentication_noop_by_unauthenticated_normal_user(factories, client):
    url = reverse('admin:login')
    user = factories.UserFactory(password='secret')
    response = client.post(url, {
        'username': user.email,
        'password': 'secret',
    })
    assert response.status_code == status.HTTP_200_OK

