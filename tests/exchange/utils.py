def assert_is_active(thing):
    assert thing in thing.__class__.objects.is_active()
    assert thing not in thing.__class__.objects.is_reserved()
    assert thing not in thing.__class__.objects.is_fulfilled()

    assert thing.is_active
    assert not thing.is_reserved
    assert not thing.is_fulfilled


def assert_is_reserved(thing):
    assert thing not in thing.__class__.objects.is_active()
    assert thing in thing.__class__.objects.is_reserved()
    assert thing not in thing.__class__.objects.is_fulfilled()

    assert not thing.is_active
    assert thing.is_reserved
    assert not thing.is_fulfilled


def assert_is_fulfilled(thing):
    assert thing not in thing.__class__.objects.is_active()
    assert thing not in thing.__class__.objects.is_reserved()
    assert thing in thing.__class__.objects.is_fulfilled()

    assert not thing.is_active
    assert not thing.is_reserved
    assert thing.is_fulfilled


def assert_not_active_not_reserved_not_fulfilled(thing):
    assert thing not in thing.__class__.objects.is_active()
    assert thing not in thing.__class__.objects.is_reserved()
    assert thing not in thing.__class__.objects.is_fulfilled()

    assert not thing.is_active
    assert not thing.is_reserved
    assert not thing.is_fulfilled
