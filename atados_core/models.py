from django.db import models
from django.utils.translation import ugettext_lazy as _


WEEKDAYS = (
        (1, _('Monday')),
        (2, _('Tuesday')),
        (3, _('Wednesday')),
        (4, _('Thursday')),
        (5, _('Friday')),
        (6, _('Saturday')),
        (0, _('Sunday')),
)

PERIODS = (
        (0, _('Morning')),
        (1, _('Afternoon')),
        (2, _('Evening')),
)


class Availability(models.Model):
    weekday = models.PositiveSmallIntegerField(_('weekday'), choices=WEEKDAYS)
    period = models.PositiveSmallIntegerField(_('period'), choices=PERIODS)

    def __unicode__(self):
        return _('%(weekday)s at %(period)s') % {'weekday': self.get_weekday_display(), 'period': self.get_period_display()}

class Cause(models.Model):
    name = models.CharField(_('name'), max_length=30)

    def __unicode__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(_('name'), max_length=30)

    def __unicode__(self):
        return self.name

class State(models.Model):
    name = models.CharField(_('name'), max_length=30)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('state')

class City(models.Model):
    name = models.CharField(_('name'), max_length=50)
    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('city')

class Suburb(models.Model):
    name = models.CharField(_('name'), max_length=30)
    city = models.ForeignKey(City)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('suburb')

class Address(models.Model):
    zipcode = models.CharField(_('Zip code'), max_length=10,
                               blank=True, null=True, default=None)
    addressline = models.CharField(_('Address line'), max_length=200,
                                  blank=True, null=True, default=None)
    addressnumber = models.CharField(_('Address number'), max_length=10,
                                  blank=True, null=True, default=None)
    neighborhood = models.CharField(_('Neighborhood'), max_length=50,
                                    blank=True, null=True, default=None)
    state = models.ForeignKey(State, verbose_name=_('State'), blank=True,
                              null=True, default=None)
    city = models.ForeignKey(City, verbose_name=_('City'), blank=True,
                             null=True, default=None)
    suburb = models.ForeignKey(Suburb, verbose_name=_('Suburb'), blank=True,
                               null=True, default=None)
