from ladder.apps.exchange.admin.forms import (
    TicketMatchTerminationForm,
)


def test_form_requires_one_of_request_or_offer():
    form = TicketMatchTerminationForm(data={})
    assert not form.is_valid()


def test_form_terminating_request():
    form = TicketMatchTerminationForm(data={
        'terminate_request': True,
    })
    assert form.is_valid(), form.errors


def test_form_terminating_offer():
    form = TicketMatchTerminationForm(data={
        'terminate_offer': True,
    })
    assert form.is_valid(), form.errors


def test_form_terminating_both():
    form = TicketMatchTerminationForm(data={
        'terminate_offer': True,
        'terminate_request': True,
    })
    assert form.is_valid(), form.errors
