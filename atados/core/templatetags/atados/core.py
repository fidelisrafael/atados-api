from django import template
from django.template import Context
from django.template.loader import get_template
from atados.core.models import Availability, WEEKDAYS, PERIODS
import re


register = template.Library()

@register.simple_tag
def active(request, href):
    if re.search(href, request.path):
        return 'active'
    return ''

@register.filter
def as_availabilities_table(selected):
    availabilities = dict([(weekday_id, {'weekday_label': weekday_label, 'periods': {}})
        for weekday_id, weekday_label in WEEKDAYS])
    for availability in Availability.objects.all():
        availabilities[availability.weekday]['periods'].update(
                {availability.period: availability in selected.all()})

    return get_template("atados/core/availabilities_table.html").render(
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

    return get_template("atados/core/availabilities_field.html").render(
        Context({
            'field': field,
            'availabilities': availabilities,
            'periods': PERIODS,
            'weekdays': WEEKDAYS,
        })
    )

@register.filter
def as_select_button_list_field(field):
    return get_template("atados/core/select_button_list_field.html").render(
        Context({
            'field': field,
        })
    )
