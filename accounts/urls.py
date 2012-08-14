from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('accounts.views',
        #url(r'^/$', 'account_dashboard', name='dashboard'),
        url(r'^new-user/$', 'new_user', name='new_user'),
        url(r'^new-user-success/$', TemplateView.as_view(template_name='registration/success.html'), name='new_user_success'),
    )
