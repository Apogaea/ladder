from django.core.urlresolvers import reverse

from rest_framework import status


def test_request_termination(factories, admin_webtest_client, models):
    ticket_request = factories.TicketRequestFactory()

    detail_url = reverse("admin:request-detail", kwargs={'pk': ticket_request.pk})

    response = admin_webtest_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK

    terminate_response = response.forms['request-terminate'].submit()
    assert terminate_response.status_code == status.HTTP_302_FOUND
    assert terminate_response.location.endswith(detail_url)

    updated_ticket_request = models.TicketRequest.objects.get(pk=ticket_request.pk)
    assert updated_ticket_request.is_terminated


def test_request_undoing_termination(factories, admin_webtest_client, models):
    ticket_request = factories.TicketRequestFactory(is_terminated=True)

    detail_url = reverse("admin:request-detail", kwargs={'pk': ticket_request.pk})

    response = admin_webtest_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK

    reverse_terminate_response = response.forms['request-terminate'].submit()
    assert reverse_terminate_response.status_code == status.HTTP_302_FOUND
    assert reverse_terminate_response.location.endswith(detail_url)

    updated_ticket_request = models.TicketRequest.objects.get(pk=ticket_request.pk)
    assert not updated_ticket_request.is_terminated
