from django.conf.urls import patterns, url

from ladder.apps.exchange.admin import views


urlpatterns = patterns('',  # NOQA
    # Ticket Offers
    url(r'^offers/$', views.AdminOfferListView.as_view(), name='offer-list'),
    url(r'^offers/(?P<pk>\d+)/$', views.AdminOfferDetailView.as_view(), name='offer-detail'),
    url(
        r'^offers/(?P<pk>\d+)/toggle-terminate/$',
        views.AdminOfferToggleTerminateView.as_view(),
        name='offer-toggle-terminate',
    ),

    # Ticket Requests
    url(r'^requests/$', views.AdminRequestListView.as_view(), name='request-list'),
    url(
        r'^requests/(?P<pk>\d+)/$',
        views.AdminRequestDetailView.as_view(),
        name='request-detail',
    ),
    url(
        r'^requests/(?P<pk>\d+)/toggle-terminate/$',
        views.AdminRequestToggleTerminateView.as_view(),
        name='request-toggle-terminate',
    ),

    # Ticket Matches
    url(r'^matches/$', views.AdminMatchListView.as_view(), name='match-list'),
    url(r'^matches/(?P<pk>\d+)/$', views.AdminMatchDetailView.as_view(), name='match-detail'),
    url(
        r'^matches/(?P<pk>\d+)/toggle-terminate/$',
        views.AdminMatchToggleTerminateView.as_view(),
        name='match-toggle-terminate',
    ),
)
