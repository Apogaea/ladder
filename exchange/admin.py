from django.contrib import admin

from exchange.models import (
    TicketRequest, TicketOffer, TicketMatch, LadderProfile, PhoneNumber,
)


admin.site.register(TicketRequest)
admin.site.register(TicketOffer)
admin.site.register(TicketMatch)
admin.site.register(LadderProfile)
