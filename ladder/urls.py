from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from accounts.forms import AuthenticationForm


admin.autodiscover()

urlpatterns = patterns('',
    url('^robots.txt$', 'django.views.generic.simple.direct_to_template', {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    # url('^sitemap.xml$', 'django.views.generic.simple.direct_to_template', {'template': 'sitemap.xml', 'mimetype': 'application/xml'}),

    # Site Urls
    url(r'^$', 'ladder.views.index', name='site_index'),
    #url(r'^ladder/', include('ladder.foo.urls')),
)

    # Auth Urls
urlpatterns += patterns('django.contrib.auth.views',
        url(r'^login/$', 'login', {'authentication_form': AuthenticationForm}, name='login'),
        url(r'^logout/$', 'logout_then_login'),
        url(r'^logged-out/$', 'logout'),
        url(r'^reset/$', 'password_reset'),
        url(r'^reset-done/$', 'password_reset_done'),
        url(r'^reset-confirm/(?P<uidb36>\w+)/(?P<token>[-a-zA-Z0-9]+)/$', 'password_reset_confirm'),
        url(r'^reset-complete/$', 'password_reset_complete'),
    )


urlpatterns += patterns('',
    # Accounts Urls
    url(r'^account/', include('accounts.urls')),

    # Exchange Urls
    url(r'^exchange/', include('exchange.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Social Auth Urls
    url(r'', include('social_auth.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
