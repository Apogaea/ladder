from django.core.urlresolvers import reverse

from rest_framework import status


def test_ticket_request_page(admin_client, factories):
    ticket_request = factories.TicketRequestFactory()

    detail_url = reverse("admin:request-detail", kwargs={'pk': ticket_request.pk})

    response = admin_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK
