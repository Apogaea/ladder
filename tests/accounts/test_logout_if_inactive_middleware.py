from django.core.urlresolvers import reverse

from rest_framework import status

def test_user_who_is_deactivated_gets_logged_out(user_client):
    user = user_client.user
    url = reverse('dashboard')

    login_url = reverse('login')

    assert user.is_active

    assert user_client.get(url).status_code == status.HTTP_200_OK

    user.is_active = False
    user.save()

    response = user_client.get(url)
    assert response.status_code == status.HTTP_302_FOUND
    assert response.get('location', '').partition('?')[0].endswith(login_url)
