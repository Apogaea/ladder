from django import template

from fusionbox.core.templatetags.fusionbox_tags import json

register = template.Library()


@register.filter
def objectify(val):
    return val.replace('-', '.')


@register.simple_tag
def ng(val):
    return "{{{{ {0} }}}}".format(val)


@register.simple_tag
def ng_rangepicker(default, values):
    return json([ng_field(default), ng_field(values)])


def ng_field(field):
    # Base Field Data
    return {
        'html_name': field.html_name,
        'name': field.name,
        'label': field.label,
        'is_required': field.field.required,
        'help_text': field.help_text,
        'initial': field.field.initial,
        'value': field.value(),
        'css_classes': field.css_classes(),
        'errors': field.errors,
        'id': field.auto_id,
        'is_hidden': field.is_hidden,
    }

register.filter('ng_field', lambda f: json(ng_field(f)))


def ng_form(form):
    data = {
        'fields': [ng_field(field) for field in form.fields],
        'prefix': form.prefix,
        'instial': form.initial,
        'is_bound': form.is_bound,
    }
    data['visible_fields'] = filter(lambda v: not v['is_hidden'], data['fields'])
    data['hidden_fields'] = filter(lambda v: v['is_hidden'], data['fields'])
    return data

register.filter('ng_form', lambda f: json(ng_form(f)))


def ng_formset(formset):
    return {
        'can_delete': formset.can_delete,
        'max_num': formset.max_num,
        'total_form_count': formset.total_form_count(),
        'empty_form': ng_form(formset.empty_form),
        'management_form': ng_form(formset.management_form),
        'forms': [ng_form(form) for form in formset.forms],
    }

register.filter('ng_formset', lambda f: json(ng_formset(f)))
