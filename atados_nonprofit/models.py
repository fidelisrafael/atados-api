from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from atados_core.models import Cause, Address
from sorl.thumbnail import ImageField
from time import time


class Nonprofit(models.Model):
    user = models.ForeignKey(User)
    causes = models.ManyToManyField(Cause, blank=True, null=True)
    name = models.CharField(_('Name'), max_length=50)
    slug = models.SlugField(max_length=50)
    details = models.TextField(_('Details'), max_length=1024, blank=True,
                               null=True, default=None)
    phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True, default=None)
    address = models.OneToOneField(Address, blank=True, null=True)
    published = models.BooleanField(_("Published"), default=False)

    def image_name(self, filename):
        left_path, extension = filename.rsplit('.', 1)
        return 'nonprofit/%s/%s.%s' % (time(), self.slug, extension)

    image = ImageField(upload_to=image_name, blank=True,
                       null=True, default=None)

    def cover_name(self, filename):
        left_path, extension = filename.rsplit('.', 1)
        return 'nonprofit-cover/%s/%s.%s' % (time(), self.slug, extension)

    cover = ImageField(upload_to=cover_name, blank=True,
                       null=True, default=None)

    @models.permalink
    def get_absolute_url(self):
        return ('slug', (self.slug,))

    def __unicode__(self):
        return self.name
