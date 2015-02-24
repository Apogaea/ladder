from django.core.urlresolvers import reverse

from rest_framework import status


def test_ticket_match_page(admin_client, factories):
    ticket_match = factories.TicketMatchFactory()

    detail_url = reverse("admin:match-detail", kwargs={'pk': ticket_match.pk})

    response = admin_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK
