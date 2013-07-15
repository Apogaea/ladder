from django.conf.urls import patterns, url

urlpatterns = patterns(
    'accounts.views',
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^edit/$', 'account_edit', name='account_edit'),
    url(r'^verify-email/(?P<uidb36>\w+)/(?P<token>[-a-zA-Z0-9]+)/$', 'verify_email'),
)
