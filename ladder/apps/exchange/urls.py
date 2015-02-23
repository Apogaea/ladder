from django.conf.urls import patterns, url

from ladder.apps.exchange import views


urlpatterns = patterns(
    'exchange.views',
    # Offers
    url(r'^offer/create/$', views.OfferCreateView.as_view(), name='offer_create'),
    url(r'^offer/(?P<pk>\d+)/$', views.OfferDetailView.as_view(), name='offer_detail'),
    url(
        r'^offer/(?P<pk>\d+)/cancel/$', views.OfferCancelView.as_view(),
        name='offer_cancel',
    ),
    url(
        r'^offer/(?P<pk>\d+)/select-recipient/$',
        views.OfferSelectRecipientView.as_view(),
        name='offer_select_recipient',
    ),
    url(
        r'^offer/(?P<pk>\d+)/toggle-automatch/$',
        views.OfferToggleAutomatchView.as_view(),
        name='offer_toggle_automatch',
    ),

    # Match
    url(
        r'^match/(?P<pk>\d+)/$', views.MatchDetailView.as_view(),
        name='match_detail',
    ),
    url(
        r'^match/(?P<pk>\d+)/confirm/$',
        views.ConfirmTicketOfferView.as_view(), name='match_confirm',
    ),

    # Requests
    url(r'^request/create/$', views.RequestCreateView.as_view(), name='request_create'),
    url(
        r'^request/(?P<pk>\d+)/$', views.RequestDetailView.as_view(),
        name='request_detail',
    ),
    url(
        r'^request/(?P<pk>\d+)/cancel/$', views.RequestCancelView.as_view(),
        name='request_cancel',
    ),
    url(
        r'^request/(?P<pk>\d+)/edit-request/$',
        views.RequestUpdateView.as_view(), name='request_update',
    ),
)
