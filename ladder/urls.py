from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = patterns(
    '',
    url(
        '^robots.txt$', TemplateView.as_view(
            content_type='text/plain',
            template_name='robots.txt',
        ),
    ),

    # Site Urls
    url(r'^$', 'ladder.views.index', name='site_index'),
)

# Auth Urls
urlpatterns += patterns(
    'authtools.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout_then_login', name='logout'),
    url(r'^password-reset/$', 'password_reset', name='password-reset'),
    url(r'^password-reset-done/$', 'password_reset_done'),
    url(
        r'^password-reset-confirm/(?P<uidb36>\w+)/(?P<token>[-a-zA-Z0-9]+)/$',
        'password_reset_confirm_and_login',
    ),
    url(r'^password-reset-complete/$', 'password_reset_complete'),
)

urlpatterns += patterns(
    '',
    # Accounts Urls
    url(r'^account/', include('accounts.urls')),

    # Exchange Urls
    url(r'^exchange/', include('exchange.urls')),

    # Admin Urls
    url(r'^admin/', include('ladder.admin.urls', namespace='admin')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
