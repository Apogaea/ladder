from django.core.urlresolvers import reverse

from rest_framework import status


def test_ticket_offer_page(admin_client, factories):
    ticket_offer = factories.TicketOfferFactory()

    detail_url = reverse("admin:offer-detail", kwargs={'pk': ticket_offer.pk})

    response = admin_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK
