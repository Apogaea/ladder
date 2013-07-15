from django.conf.urls import patterns, url

urlpatterns = patterns(
    'exchange.views',
    # Offers
    url(r'^offer-ticket/$', 'offer_create', name='offer_create'),
    url(r'^offer-status/(?P<pk>\d+)/$', 'offer_detail', name='offer_detail'),
    url(r'^offer-status/(?P<pk>\d+)/select-recipient/$', 'offer_select_recipient', name='offer_select_recipient'),

    # Requests
    url(r'^request-ticket/$', 'request_create', name='request_create'),
    url(r'^request-status/(?P<pk>\d+)/$', 'request_detail', name='request_detail'),
    url(r'^request-status/(?P<pk>\d+)/edit-request/$', 'request_edit', name='request_edit'),
)
