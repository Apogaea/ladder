from ladder.apps.exchange.models import TicketRequest


def exchange_stats(request):
    return {
        'num_active_requests': TicketRequest.objects.is_active().count(),
        'num_fulfilled_requests': TicketRequest.objects.is_fulfilled().count(),
    }
