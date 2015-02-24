import urllib

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def update_querystring(context, **kwargs):
    # We want to override the parameters, but querydict doesn't:
    # >>> qs.update(p=1)
    # <QueryDict: {u'p': [1]>
    # >>> qs.update(p=2)
    # <QueryDict: {u'p': [1, 2]}>

    # So we convert the querydict to dict.
    # The downside of this is that we lose data for the querystring:
    #   foo=bar&foo=bar2
    qs = context['request'].GET.dict()
    qs.update(kwargs)
    return urllib.urlencode(qs)
