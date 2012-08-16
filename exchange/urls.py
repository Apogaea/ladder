from django.conf.urls import patterns, url

urlpatterns = patterns('exchange.views',
        #url(r'^$', 'dashboard', name='dashboard'),
        url(r'^offer-ticket/$', 'offer_ticket', name='offer_ticket'),
        url(r'^request-ticket/$', 'request_ticket', name='request_ticket'),
    )
