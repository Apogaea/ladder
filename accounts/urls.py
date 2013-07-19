from django.conf.urls import patterns, url

urlpatterns = patterns(
    'accounts.views',
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^edit/$', 'account_edit', name='account_edit'),
    url(r'^verify-email/(?P<uidb36>\w+)/(?P<token>[-a-zA-Z0-9]+)/$', 'verify_email'),
)

urlpatterns += patterns(
    'exchange.views',
    url(r'^phone-number/add/$', 'create_phone_number', name='create_phone_number'),
    url(r'^phone-number/(?P<pk>\d+)/verify/$', 'verify_phone_number', name='verify_phone_number'),
    url(r'^phone-number/(?P<pk>\d+)/delete/$', 'delete_phone_number', name='delete_phone_number'),
    url(r'^phone-number/(?P<pk>\d+)/send-confirmation-code/$', 'send_confirmation_code', name='send_confirmation_code'),
    url(r'^phone-number/(?P<pk>\d+)/set-as-primary/$', 'set_primary_phone_number', name='set_primary_phone_number'),
)
