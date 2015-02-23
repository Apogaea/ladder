from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static

from ladder.core import views


urlpatterns = patterns(
    '',
    url(
        '^robots.txt$', TemplateView.as_view(
            content_type='text/plain',
            template_name='robots.txt',
        ),
    ),

    # Site Urls
    url(r'^$', views.SiteIndexView.as_view(), name='site_index'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^faq/$', views.FAQView.as_view(), name='faq'),
)

# Auth Urls
urlpatterns += patterns(
    'authtools.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout_then_login', name='logout'),
    url(r'^password-reset/$', 'password_reset', name='password_reset'),
    url(
        r'^password-reset-done/$', 'password_reset_done',
        name='password_reset_done',
    ),
    url(
        r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'password_reset_confirm_and_login',
        name='password_reset_confirm_and_login',
    ),
    url(
        r'^password-reset-complete/$', 'password_reset_complete',
        name='password_reset_complete',
    ),
)

urlpatterns += patterns(
    '',
    # Accounts Urls
    url(r'^account/', include('ladder.apps.accounts.urls')),

    # Exchange Urls
    url(r'^exchange/', include('ladder.apps.exchange.urls')),

    # Admin Urls
    url(r'^admin/', include('ladder.core.admin.urls', namespace='admin')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',  # NOQA
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
