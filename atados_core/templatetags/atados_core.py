import os
from django import template
from django.template import Context
from django.template.defaulttags import kwarg_re
from django.template.loader import get_template
from django.utils.encoding import smart_str
import re


register = template.Library()

@register.simple_tag
def active(request, href):
    if re.search(href, request.path):
        return 'active'
    return ''

@register.filter
def as_availabilities_table(selected):
    return 'availabilities'

@register.filter
def as_availabilities_field(field):
    return 'availabilities'

@register.filter
def as_select_button_list_field(field):
    return get_template("atados_core/select_button_list_field.html").render(
        Context({
            'field': field,
        })
    )

class SearchQueryNode(template.Node):

    def  __init__(self, kwargs):
        self.kwargs = kwargs

    def render(self, context):
        kwargs = dict([(smart_str(k, 'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])

        params = {'q': context['form']['q'].value()}

        if context['form']['types'].value():
            params['types'] = context['form']['types'].value()[0]

        if context['form']['causes'].value():
            params['causes'] = context['form']['causes'].value()[0]

        if context['form']['skills'].value():
            params['skills'] = context['form']['skills'].value()[0]

        params = dict(params.items() + kwargs.items())

        params = ['%s=%s' % (key, value) for key, value in params.iteritems() if value]

        return '?' + '&'.join(params)

@register.tag
def search_query(parser, token):
    bits = token.split_contents()[1:]
    kwargs = {}
    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to search_query tag")
            name, value = match.groups()
            kwargs[name] = parser.compile_filter(value)

    return SearchQueryNode(kwargs)
