from django.core.urlresolvers import reverse

from rest_framework import status


def test_admin_user_detail_page(factories, admin_client):
    user = factories.UserWithProfileFactory()

    response = admin_client.get(reverse(
        'admin:user-detail', kwargs={'pk': user.pk},
    ))
    assert response.status_code == status.HTTP_200_OK


def test_admin_change_user(factories, admin_client, User):
    user = factories.UserWithProfileFactory(
        _profile__phone_number='555-444-3333',
        email='original@example.com',
        display_name='original',
        is_active=True,
        is_superuser=True,
    )
    url = reverse('admin:user-change', kwargs={'pk': user.pk})

    response = admin_client.post(url, {
        'phone_number': '555-555-5555',
        'email': 'test-email@example.com',
        'display_name': 'test-display_name',
        'is_active': False,
        'is_superuser': False,
    })
    expected_location = reverse('admin:user-detail', kwargs={'pk': user.pk})
    assert response.get('location', '').endswith(expected_location)

    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.email == 'test-email@example.com'
    assert updated_user.display_name == 'test-display_name'
    assert updated_user.profile.phone_number == '555-555-5555'
    assert not updated_user.is_active
    assert not updated_user.is_superuser
