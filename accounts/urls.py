from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
        url(r'^$', 'dashboard', name='dashboard'),
        url(r'^edit/$', 'account_edit', name='account_edit'),
    )
