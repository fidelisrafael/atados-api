from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from atados_core.models import Cause, Skill, Address
from sorl.thumbnail import ImageField
from time import time


class Volunteer(models.Model):
    user = models.ForeignKey(User)
    causes = models.ManyToManyField(Cause, blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True, null=True)
    address = models.OneToOneField(Address, blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True,
                             default=None)

    def image_name(self, filename):
        left_path, extension = filename.rsplit('.', 1)
        return 'volunteer/%s/%s/%s.%s' % (self.user.username,
                                          time(),
                                          self.user.username,
                                          extension)

    image = ImageField(upload_to=image_name, blank=True,
                       null=True, default=None)

    @models.permalink
    def get_absolute_url(self):
        return ('slug', (self.user.username,))

    def __unicode__(self):
        return self.user.first_name

def create_volunteer(sender, instance, created, **kwargs):  
    if created:  
       profile, created = Volunteer.objects.get_or_create(user=instance)

post_save.connect(create_volunteer, sender=User)
