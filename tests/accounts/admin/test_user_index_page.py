from django.core.urlresolvers import reverse

from rest_framework import status


def test_admin_user_index_page(admin_client, factories):
    factories.UserWithProfileFactory.create_batch(20)

    response = admin_client.get(reverse('admin:user-list'))
    assert response.status_code == status.HTTP_200_OK
