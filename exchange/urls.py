from django.conf.urls import patterns, url

urlpatterns = patterns('exchange.views',
        # Listings
        url(r'^list-ticket/$', 'listing_create', name='listing_create'),
        url(r'^listing-status/(?P<pk>\d+)/$', 'listing_detail', name='listing_detail'),

        # Requests
        url(r'^request-ticket/$', 'request_create', name='request_create'),
        url(r'^request-status/$', 'request_detail', name='request_detail'),
    )
