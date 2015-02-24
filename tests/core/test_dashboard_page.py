from django.core.urlresolvers import reverse

from rest_framework import status


def test_dashboard_page(user_client, factories):
    response = user_client.get(reverse('dashboard'))
    assert response.status_code == status.HTTP_200_OK
