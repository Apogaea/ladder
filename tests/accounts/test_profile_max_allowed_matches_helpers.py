def test_user_max_allowed_matches_api(factories):
    user = factories.UserWithProfileFactory()
    user.profile.max_allowed_matches = 2
    user.profile.save()

    assert not user.profile.has_reached_max_allowed_matches
    assert user.profile.can_offer_ticket

    # these should not count
    factories.TicketOfferFactory(user=user, is_cancelled=True)
    factories.TicketOfferFactory(user=user, is_cancelled=True)

    assert not user.profile.has_reached_max_allowed_matches
    assert user.profile.can_offer_ticket

    # these should not count
    factories.TicketOfferFactory(user=user, is_terminated=True)
    factories.TicketOfferFactory(user=user, is_terminated=True)

    assert not user.profile.has_reached_max_allowed_matches
    assert user.profile.can_offer_ticket


def test_expired_matches_consume_max_matches(factories):
    user = factories.UserWithProfileFactory()
    user.profile.max_allowed_matches = 2
    user.profile.save()

    assert not user.profile.has_reached_max_allowed_matches
    assert user.profile.can_offer_ticket

    # these should count.
    factories.ExpiredTicketMatchFactory(ticket_offer__user=user)
    factories.ExpiredTicketMatchFactory(ticket_offer__user=user)

    assert user.profile.has_reached_max_allowed_matches
    assert not user.profile.can_offer_ticket


def test_accepted_matches_consume_max_matches(factories):
    user = factories.UserWithProfileFactory()
    user.profile.max_allowed_matches = 2
    user.profile.save()

    assert not user.profile.has_reached_max_allowed_matches
    assert user.profile.can_offer_ticket

    # these should count.
    factories.AcceptedTicketMatchFactory(ticket_offer__user=user)
    factories.AcceptedTicketMatchFactory(ticket_offer__user=user)

    assert user.profile.has_reached_max_allowed_matches
    assert not user.profile.can_offer_ticket


def test_pending_matches_consume_max_matches(factories):
    user = factories.UserWithProfileFactory()
    user.profile.max_allowed_matches = 2
    user.profile.save()

    assert not user.profile.has_reached_max_allowed_matches
    assert user.profile.can_offer_ticket

    # these should count.
    factories.TicketMatchFactory(ticket_offer__user=user)
    factories.TicketMatchFactory(ticket_offer__user=user)

    assert user.profile.has_reached_max_allowed_matches
    assert not user.profile.can_offer_ticket
