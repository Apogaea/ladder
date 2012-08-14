from django.views.generic.base import TemplateView


class SiteIndexView(TemplateView):
    template_name = 'index.html'

index = SiteIndexView.as_view()
