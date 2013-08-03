import os
from django import template
from django.template import Context
from django.template.defaulttags import kwarg_re
from django.template.loader import get_template
from django.utils import formats
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from atados_core.models import Availability, WEEKDAYS, PERIODS
from atados_project.models import Apply
import re


register = template.Library()

@register.simple_tag
def active(request, href):
    if re.search(href, request.path):
        return 'active'
    return ''

@register.filter
def as_location_string(address):
    if address == None:
        return ''

    locations = []

    if address.state:
        if address.city:
            if address.suburb:
                locations.append(str(address.suburb))
            locations.append(str(address.city))
        locations.append(str(address.state))
    
    return ' - '.join(locations)

@register.filter
def as_availabilities_table(selected):
    availabilities = dict([(weekday_id, {'weekday_label': weekday_label, 'periods': {}})
        for weekday_id, weekday_label in WEEKDAYS])
    for availability in Availability.objects.all():
        availabilities[availability.weekday]['periods'].update(
                {availability.period: availability in selected.all()})

    return get_template("atados_core/availabilities_table.html").render(
        Context({
            'availabilities': availabilities,
            'periods': PERIODS,
            'weekdays': WEEKDAYS,
        })
    )

@register.filter
def as_availabilities_field(field):
    availabilities = dict([(weekday_id, {'weekday_label': weekday_label, 'periods': {}})
        for weekday_id, weekday_label in WEEKDAYS])
    for availability in Availability.objects.all():
        availabilities[availability.weekday]['periods'].update(
                {availability.period: availability.id})

    return get_template("atados_core/availabilities_field.html").render(
        Context({
            'field': field,
            'availabilities': availabilities,
            'periods': PERIODS,
            'weekdays': WEEKDAYS,
        })
    )

@register.filter
def as_multi_select_list_field(field):
    return get_template("atados_core/multi_select_list_field.html").render(
        Context({
            'field': field,
        })
    )

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

@register.filter
def as_activity_li(model):
    if isinstance(model, Apply):
        icon='heart'
        date=model.date
        html=_('<a href="%(volunteer_url)s">%(volunteer)s</a> applied to <a href="%(project_url)s">%(project)s</a>.') % {'project_url': model.project.get_absolute_url(),
                                                                'volunteer': model.volunteer.user.first_name,
                                                                'volunteer_url': model.volunteer.get_absolute_url(),
                                                                'project': model.project.name}

    if icon and date and html:
        date = formats.date_format(date, "DATE_FORMAT")
        return mark_safe('<li><i class="icon icon-%s"></i> <span class="date">%s</span> - %s</li>' % (icon, date, html))
    return ''
