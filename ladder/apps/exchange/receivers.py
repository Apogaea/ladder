def create_creation_history_entry(sender, instance, created, raw, **kwargs):
    if not created or raw:
        return

    instance.history.create(
        message="Ticket Request created.",
    )


def create_cancellation_history_entry(sender, instance, raw, **kwargs):
    if raw or instance.pk is None:
        return

    is_currently_cancelled = sender.objects.filter(
        pk=instance.pk, is_cancelled=True,
    ).exists()

    if is_currently_cancelled:
        return

    if instance.is_cancelled:
        instance.history.create(
            message="Ticket Request cancelled."
        )


def create_termination_history_entry(sender, instance, raw, **kwargs):
    if raw or instance.pk is None:
        return

    is_currently_terminated = sender.objects.filter(
        pk=instance.pk, is_terminated=True,
    ).exists()

    if is_currently_terminated is not instance.is_terminated:
        if is_currently_terminated:
            suffix = "termination reversed"
        else:
            suffix = "terminated"
        instance.history.create(
            message="Ticket Request {0}.".format(suffix)
        )


def create_match_creation_history_entries(sender, instance, created, raw, **kwargs):
    if not created or raw:
        return

    message = "Ticket Match #{0} created".format(instance.pk)
    instance.ticket_request.history.create(message=message)
    instance.ticket_offer.history.create(message=message)


def create_match_confirmation_history_entries(sender, instance, raw, **kwargs):
    if raw or instance.pk is None:
        return

    not_currently_accepted = sender.objects.filter(
        pk=instance.pk, accepted_at__isnull=True,
    ).exists()

    if not_currently_accepted and instance.is_accepted:
        message = "Ticket Match #{0} confirmed".format(instance.pk)
        instance.ticket_request.history.create(message=message)
        instance.ticket_offer.history.create(message=message)


def create_match_termination_history_entries(sender, instance, raw, **kwargs):
    if raw or instance.pk is None:
        return

    is_currently_terminated = sender.objects.filter(
        pk=instance.pk, is_terminated=True,
    ).exists()

    if is_currently_terminated is not instance.is_terminated:
        if is_currently_terminated:
            suffix = "termination reversed"
        else:
            suffix = "terminated"
        message = "Ticket Match #{0} {1}".format(instance.pk, suffix)
        instance.ticket_request.history.create(message=message)
        instance.ticket_offer.history.create(message=message)
