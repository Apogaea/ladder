from django.core.urlresolvers import reverse

from rest_framework import status


def test_ticket_request_list_page(admin_client, factories):
    factories.TicketRequestFactory.create_batch(15)

    list_url = reverse("admin:request-list")

    response = admin_client.get(list_url)
    assert response.status_code == status.HTTP_200_OK
