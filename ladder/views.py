from django.views.generic.base import TemplateView


class SiteIndexView(TemplateView):
    template_name = 'index.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class FAQView(TemplateView):
    template_name = 'faq.html'
