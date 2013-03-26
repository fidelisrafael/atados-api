from django.db import models
from django.utils.translation import ugettext_lazy as _
from atados.core.models import Availability, Cause, Skill, State, City, Suburb
from atados.nonprofit.models import Nonprofit
from atados.volunteer.models import Volunteer
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
    responsible = models.CharField(_('Responsible name'), max_length=50)
    phone = models.CharField(_('Phone'), max_length=20)
    email = models.EmailField(_('E-mail'))
    zipcode = models.CharField(_('Zip code'), max_length=10,
                               blank=True, null=True, default=None)
    addressline = models.CharField(_('Address line'), max_length=200,
                                  blank=True, null=True, default=None)
    addressnumber = models.CharField(_('Address number'), max_length=10,
                                  blank=True, null=True, default=None)
    neighborhood = models.CharField(_('Neighborhood'), max_length=50,
                                    blank=True, null=True, default=None)
    state = models.ForeignKey(State, blank=True, null=True, default=None)
    city = models.ForeignKey(City, blank=True, null=True, default=None)
    suburb = models.ForeignKey(Suburb, blank=True, null=True, default=None)
    vacancies = models.PositiveSmallIntegerField(_('Vacancies'),
                                    blank=True, null=True, default=None)
    published = models.BooleanField(_("Published"), default=False)
    deleted = models.BooleanField(_("Deleted"), default=False)
    deleted_date = models.DateTimeField(_("Deleted date"), blank=True,
                                        null=True)

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

class ProjectDonation(Project):
    objects = ProjectManager()
    project_type = 'donation'
    collection_by_nonprofit = models.BooleanField(
            _('Collection made by the nonprofit'))

class ProjectWork(Project):
    objects = ProjectManager()
    project_type = 'work'
    availabilities = models.ManyToManyField(Availability)
    prerequisites = models.TextField(_('Prerequisites'), max_length=1024)
    skills = models.ManyToManyField(Skill)
    weekly_hours = models.PositiveSmallIntegerField(_('Weekly hours'),
                                        blank=True, null=True)
    can_be_done_remotely = models.BooleanField(
            _('This work can be done remotely.'))

class ProjectJob(ProjectWork):
    objects = ProjectManager()
    project_type = 'job'

class Apply(models.Model):
    volunteer = models.ForeignKey(Volunteer)
    project = models.ForeignKey(Project)
