from django.conf.urls import patterns, url

from ladder.apps.exchange import views


urlpatterns = patterns(
    'exchange.views',
    # Offers
    url(r'^offer/create/$', views.OfferCreateView.as_view(), name='offer-create'),
    url(r'^offer/(?P<pk>\d+)/$', views.OfferDetailView.as_view(), name='offer-detail'),
    url(
        r'^offer/(?P<pk>\d+)/cancel/$', views.OfferCancelView.as_view(),
        name='offer-cancel',
    ),

    # Match
    url(
        r'^match/(?P<pk>\d+)/$', views.MatchDetailView.as_view(),
        name='match-detail',
    ),
    url(
        r'^match/(?P<pk>\d+)/confirm/$',
        views.ConfirmTicketOfferView.as_view(), name='match-confirm',
    ),

    # Requests
    url(r'^request/create/$', views.RequestCreateView.as_view(), name='request-create'),
    url(
        r'^request/(?P<pk>\d+)/$', views.RequestDetailView.as_view(),
        name='request-detail',
    ),
    url(
        r'^request/(?P<pk>\d+)/cancel/$', views.RequestCancelView.as_view(),
        name='request-cancel',
    ),
    url(
        r'^request/(?P<pk>\d+)/edit-request/$',
        views.RequestUpdateView.as_view(), name='request-update',
    ),
)
