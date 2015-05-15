def test_special_case(factories, models):
    offer = factories.TicketOfferFactory()

    factories.ExpiredTicketMatchFactory(ticket_offer=offer)
    factories.ExpiredTicketMatchFactory(ticket_offer=offer)

    m_1 = factories.TicketMatchFactory(ticket_offer=offer)
    m_1.ticket_request.is_cancelled = True
    m_1.ticket_request.save()

    assert offer.is_active
    assert offer in models.TicketOffer.objects.is_active()
