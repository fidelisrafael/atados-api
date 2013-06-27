from django.db import models
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from atados_core.models import Availability, Cause, Skill, Address
from atados_nonprofit.models import Nonprofit
from atados_volunteer.models import Volunteer
from sorl.thumbnail import ImageField
from time import time
from datetime import datetime


class ProjectManager(models.Manager):
    use_for_related_fields = True

    def active(self):
        return self.get_query_set().filter(deleted=False)

    def published(self):
        return self.get_query_set().active(published=True)


class Project(models.Model):
    objects = ProjectManager()
    nonprofit = models.ForeignKey(Nonprofit)
    causes = models.ManyToManyField(Cause)
    name = models.CharField(_('Project name'), max_length=50)
    slug = models.SlugField(max_length=50)
    details = models.TextField(_('Details'), max_length=1024)
    description = models.TextField(_('Short description'), max_length=75,
                                   blank=True, null=True)
    responsible = models.CharField(_('Responsible name'), max_length=50,
                                   blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True)
    email = models.EmailField(_('E-mail'), blank=True, null=True)
    published = models.BooleanField(_("Published"), default=False)
    closed = models.BooleanField(_("Closed"), default=False)
    deleted = models.BooleanField(_("Deleted"), default=False)
    deleted_date = models.DateTimeField(_("Deleted date"), blank=True,
                                        null=True)

    def get_description(self):
        return self.description if self.description else Truncator(
                self.details).chars(75)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.deleted_date = datetime.now()
        self.save()

    def image_name(self, filename):
        left_path, extension = filename.rsplit('.', 1)
        return 'project/%s/%s/%s.%s' % (self.nonprofit.slug,
                                        time(), self.slug, extension)

    image = ImageField(upload_to=image_name, blank=True,
                       null=True, default=None)

    def __unicode__(self):
        return  '%s - %s' % (self.name, self.nonprofit.name)

    @models.permalink
    def get_absolute_url(self):
        return ('project:details', (self.nonprofit.slug, self.slug))

    @models.permalink
    def get_edit_url(self):
        return ('project:edit', (self.nonprofit.slug, self.slug))

    @models.permalink
    def get_delete_url(self):
        return ('project:delete', (self.nonprofit.slug, self.slug))

    def get_project_type(self):
        return self.project_type

class Donation(models.Model):
    project = models.OneToOneField(Project)
    delivery = models.OneToOneField(Address)
    collection_by_nonprofit = models.BooleanField(
            _('Collection made by the nonprofit'))

class Work(models.Model):
    project = models.OneToOneField(Project)
    address = models.OneToOneField(Address)
    availabilities = models.ManyToManyField(Availability)
    skills = models.ManyToManyField(Skill)
    weekly_hours = models.PositiveSmallIntegerField(_('Weekly hours'),
                                        blank=True, null=True)
    can_be_done_remotely = models.BooleanField(
            _('This work can be done remotely.'))

class Material(models.Model):
    donation = models.ForeignKey(Donation)
    name = models.CharField(_('Material name'), max_length=50,
                            blank=True, null=True, default=None)
    quantity = models.PositiveSmallIntegerField(_('Quantity'),
                                                blank=True,
                                                null=True,
                                                default=None)

class Role(models.Model):
    work = models.ForeignKey(Work)
    name = models.CharField(_('Role name'), max_length=50,
                            blank=True, null=True, default=None)
    prerequisites = models.TextField(_('Prerequisites'), max_length=1024,
                                    blank=True, null=True, default=None)
    vacancies = models.PositiveSmallIntegerField(_('Vacancies'),
                                    blank=True, null=True, default=None)

class Apply(models.Model):
    volunteer = models.ForeignKey(Volunteer)
    project = models.ForeignKey(Project)
