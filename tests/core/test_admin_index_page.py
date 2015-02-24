from django.core.urlresolvers import reverse

from rest_framework import status


def test_admin_index_page(factories, client):
    user = factories.SuperUserFactory(password='secret')
    assert client.login(username=user.email, password='secret')

    response = client.get(reverse('admin:index'))

    assert response.status_code == status.HTTP_200_OK
