from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from atados_core.models import Cause, Skill, State, City, Suburb
from sorl.thumbnail import ImageField
from time import time


class Volunteer(models.Model):
    user = models.ForeignKey(User)
    causes = models.ManyToManyField(Cause, blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True, null=True)
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

    def image_name(self, filename):
        left_path, extension = filename.rsplit('.', 1)
        return 'volunteer/%s/%s.%s' % (time(), self.user.username, extension)

    image = ImageField(upload_to=image_name, blank=True,
                       null=True, default=None)

    @models.permalink
    def get_absolute_url(self):
        return ('slug', (self.user.username,))

    def __unicode__(self):
        return self.user.first_name

