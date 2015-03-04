from django.core.urlresolvers import reverse
from django.core import mail

from rest_framework import status


def test_request_creation_view(user_client):
    response = user_client.get(reverse('request-create'))
    assert response.status_code == status.HTTP_200_OK

    assert not user_client.user.ticket_requests.exists()

    response = user_client.post(
        reverse('request-create'), {'message': 'A nice heartfelt message'},
    )
    assert response.status_code == status.HTTP_302_FOUND

    assert user_client.user.ticket_requests.exists()


def test_automatic_request_matching(user_client, models, factories):
    factories.TicketOfferFactory()

    assert not user_client.user.ticket_requests.exists()
    assert not models.TicketMatch.objects.exists()

    assert not mail.outbox

    response = user_client.post(
        reverse('request-create'), {'message': 'A nice heartfelt message'},
    )
    assert response.status_code == status.HTTP_302_FOUND

    assert user_client.user.ticket_requests.exists()
    assert models.TicketMatch.objects.exists()
    ticket_match = models.TicketMatch.objects.get()
    expected_location = reverse('request-detail', kwargs={'pk': ticket_match.ticket_request.pk})
    assert response.get('location').endswith(expected_location)

    # one email to both offerer and recipient.
    assert len(mail.outbox) == 2
