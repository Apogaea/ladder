import pytest

from django.core.urlresolvers import reverse

from rest_framework import status


@pytest.mark.django_db
def test_anon_user_admin_access(client):
    admin_index_url = reverse('admin:index')

    response = client.get(admin_index_url)
    assert response.status_code == status.HTTP_302_FOUND
