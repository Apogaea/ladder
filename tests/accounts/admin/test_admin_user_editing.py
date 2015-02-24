from django.core.urlresolvers import reverse

from rest_framework import status


def test_updating_a_user_via_the_admin(models, admin_webtest_client, user):
    change_url = reverse('admin:user-change', kwargs={'pk': user.pk})

    response = admin_webtest_client.get(change_url)
    assert response.status_code == status.HTTP_200_OK

    response.form['email'] = 'new-email@example.com'
    response.form['phone_number'] = '123-456-7890'
    response.form['max_allowed_matches'] = '10'
    response.form['display_name'] = 'new-name'
    response.form['is_active'] = False
    response.form['is_superuser'] = True

    change_response = response.form.submit()
    assert change_response.status_code == status.HTTP_302_FOUND

    updated_user = models.User.objects.get(pk=user.pk)

    assert updated_user.email == 'new-email@example.com'
    assert updated_user.profile.phone_number == '123-456-7890'
    assert updated_user.profile.max_allowed_matches == 10
    assert updated_user.display_name == 'new-name'
    assert updated_user.is_active is False
    assert updated_user.is_superuser is True
