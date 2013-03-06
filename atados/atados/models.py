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
        return _('%s at %s') % (self.get_weekday_display(), self.get_period_display())

class Cause(models.Model):
    name = models.CharField(_('name'), max_length=30)

    def __unicode__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(_('name'), max_length=30)

    def __unicode__(self):
        return self.name
