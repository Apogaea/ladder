from django.core.management.base import BaseCommand

from ladder.apps.exchange.models import TicketMatch


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        match = TicketMatch.objects.create_match(fail_silently=True)
        if match:
            self.stdout.write(
                "Match #{0} created for TicketRequest:{1} and "
                "TicketOffer:{2}".format(
                    match.pk,
                    match.ticket_request_id,
                    match.ticket_offer_id,
                )
            )
