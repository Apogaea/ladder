from django.conf.urls import patterns, url

from ladder.apps.accounts.admin import views

urlpatterns = patterns('',  # NOQA
    url(
        r'^generate-pre-registration-url/$',
        views.AdminGeneratePreRegistrationLink.as_view(),
        name='generate-pre-registration-url',
    ),
    url(r'^users/$', views.AdminUserListView.as_view(), name='user-list'),
    url(r'^users/(?P<pk>\d+)/$', views.AdminUserDetailView.as_view(), name='user-detail'),
    url(
        r'^users/(?P<pk>\d+)/change/$', views.AdminUserChangeView.as_view(),
        name='user-change',
    ),
)
