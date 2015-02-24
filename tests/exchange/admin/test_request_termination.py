from django.core.urlresolvers import reverse


def test_request_termination(admin_webtest_client, factories):
    ticket_request = factories.TicketRequestFactory()

    detail_url = TODO
