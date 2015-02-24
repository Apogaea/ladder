from django.core.urlresolvers import reverse

from rest_framework import status


def test_offer_termination(factories, admin_webtest_client, models):
    ticket_offer = factories.TicketOfferFactory()

    detail_url = reverse("admin:offer-detail", kwargs={'pk': ticket_offer.pk})

    response = admin_webtest_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK

    terminate_response = response.forms['offer-terminate'].submit()
    assert terminate_response.status_code == status.HTTP_302_FOUND
    assert terminate_response.location.endswith(detail_url)

    updated_ticket_offer = models.TicketOffer.objects.get(pk=ticket_offer.pk)
    assert updated_ticket_offer.is_terminated


def test_offer_undoing_termination(factories, admin_webtest_client, models):
    ticket_offer = factories.TicketOfferFactory(is_terminated=True)

    detail_url = reverse("admin:offer-detail", kwargs={'pk': ticket_offer.pk})

    response = admin_webtest_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK

    reverse_terminate_response = response.forms['offer-terminate'].submit()
    assert reverse_terminate_response.status_code == status.HTTP_302_FOUND
    assert reverse_terminate_response.location.endswith(detail_url)

    updated_ticket_offer = models.TicketOffer.objects.get(pk=ticket_offer.pk)
    assert not updated_ticket_offer.is_terminated
