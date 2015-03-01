from django.conf.urls import patterns, url

from ladder.apps.accounts import views

urlpatterns = patterns('',  # NOQA
    url(r'^$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^register/success/$', views.RegisterSuccessView.as_view(), name='register-success'),
    url(
        r'^register/(?P<token>[-a-zA-Z0-9_:]+)/$',
        views.RegisterConfirmView.as_view(),
        name='register-confirm',
    ),
    url(
        r'^register/(?P<token>[-a-zA-Z0-9_:]+)/verify/$',
        views.RegisterVerifyPhoneNumberView.as_view(),
        name='register-verify-phone-number',
    ),
)
