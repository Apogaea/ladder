from django.conf.urls import patterns, include, url

from ladder.core.admin import views

urlpatterns = patterns('',  # NOQA
    # Main Admin Urls
    url(r'^$', views.AdminIndexView.as_view(), name='index'),
    url(r'^guide/$', views.AdminGuideView.as_view(), name='guide'),
    url(r'^login/$', views.AdminLoginView.as_view(), name='login'),

    # App Admin Urls
    url(r'^', include('ladder.apps.accounts.admin.urls')),
    url(r'^', include('ladder.apps.exchange.admin.urls')),
)
