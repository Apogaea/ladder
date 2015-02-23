from django.conf.urls import patterns, url

from ladder.apps.accounts.admin import views

urlpatterns = patterns('',  # NOQA
    url(r'^users/$', views.AdminUserListView.as_view(), name='user_list'),
    url(r'^users/(?P<pk>\d+)/$', views.AdminUserDetailView.as_view(), name='user_detail'),
    url(
        r'^users/(?P<pk>\d+)/change/$', views.AdminUserChangeView.as_view(),
        name='user_change',
    ),
)
