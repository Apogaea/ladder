from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
        url(r'^$', 'dashboard', name='dashboard'),
        url(r'^edit/$', 'account_edit', name='account_edit'),
        url(r'^verify/$', 'account_verify', name='account_verify'),
        url(r'^send-code/$', 'account_send_verification_code', name='account_send_code'),
    )
