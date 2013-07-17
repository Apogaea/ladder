from django.conf.urls import patterns, url

urlpatterns = patterns(
    'exchange.views',
    # Offers
    url(r'^offer/create/$', 'offer_create', name='offer_create'),
    url(r'^offer/(?P<pk>\d+)/status/$', 'offer_detail', name='offer_detail'),
    url(r'^offer/(?P<pk>\d+)/cancel/$', 'offer_cancel', name='offer_cancel'),
    url(r'^offer/(?P<pk>\d+)/select-recipient/$', 'offer_select_recipient', name='offer_select_recipient'),

    # Match
    url(r'^match/(?P<pk>\d+)/$', 'match_detail', name='match_detail'),
    url(r'^match/(?P<pk>\d+)/confirm/$', 'match_confirm', name='match_confirm'),

    # Requests
    url(r'^request/create/$', 'request_create', name='request_create'),
    url(r'^request/(?P<pk>\d+)/status/$', 'request_detail', name='request_detail'),
    url(r'^request/(?P<pk>\d+)/cancel/$', 'request_cancel', name='request_cancel'),
    url(r'^request/(?P<pk>\d+)/edit-request/$', 'request_edit', name='request_edit'),
)
