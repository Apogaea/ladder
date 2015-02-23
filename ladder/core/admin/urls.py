from django.conf.urls import patterns, include, url

from ladder.admin import views

urlpatterns = patterns('',  # NOQA
    # Main Admin Urls
    url(r'^$', views.AdminIndexView.as_view(), name='index'),
    url(r'^login/$', views.AdminLoginView.as_view(), name='login'),

    # App Admin Urls
    url(r'^', include('accounts.admin.urls')),
    url(r'^', include('exchange.admin.urls')),
)
