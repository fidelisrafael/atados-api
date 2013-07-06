from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from atados_core.models import Cause, Address
from atados_volunteer.models import Volunteer
from sorl.thumbnail import ImageField
from time import time


class NonprofitManager(models.Manager):
    use_for_related_fields = True

    def active(self):
        return self.get_query_set().filter(deleted=False)

    def published(self):
        return self.get_query_set().active(published=True)

class Nonprofit(models.Model):
    objects = NonprofitManager()
    user = models.ForeignKey(User)
    causes = models.ManyToManyField(Cause, blank=True, null=True)
    name = models.CharField(_('Name'), max_length=50)
    slug = models.SlugField(max_length=50)
    details = models.TextField(_('Details'), max_length=1024, blank=True,
                               null=True, default=None)
    description = models.TextField(_('Short description'), max_length=100,
                                   blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True, default=None)
    address = models.OneToOneField(Address, blank=True, null=True)
    published = models.BooleanField(_("Published"), default=False)
    deleted = models.BooleanField(_("Deleted"), default=False)
    deleted_date = models.DateTimeField(_("Deleted date"), blank=True,
                                        null=True)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.deleted_date = datetime.now()
        self.save()

    def get_description(self):
        return self.description if self.description else Truncator(
                self.details).chars(100)

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

    def get_volunteers(self):
        return Volunteer.objects.all()[:10]

    @models.permalink
    def get_absolute_url(self):
        return ('slug', (self.slug,))

    def __unicode__(self):
        return self.name
