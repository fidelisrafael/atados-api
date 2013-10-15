from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from sorl.thumbnail import ImageField
from time import time

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
    code = models.CharField(_('code'), max_length=2)

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

class NonprofitManager(models.Manager):
    use_for_related_fields = True

    def active(self):
        return self.get_query_set().filter(deleted=False)

    def published(self):
        return self.active().filter(published=True)

class Nonprofit(models.Model):
    objects = NonprofitManager()
    user = models.ForeignKey(User, related_name='nonprofit_created_by')
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

    def type(self):
      return "NONPROFIT";

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
        return Volunteer.objects.filter(apply__project__nonprofit__id=self.id)

    @models.permalink
    def get_absolute_url(self):
        return ('slug', (self.slug,))

    def __unicode__(self):
        return self.name

class Volunteer(models.Model):
    user = models.ForeignKey(User)
    causes = models.ManyToManyField(Cause, blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True, null=True)
    address = models.OneToOneField(Address, blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True,
                             default=None)

    facebook_uid = models.PositiveIntegerField(blank=True, null=True)
    facebook_access_token = models.CharField(blank=True, max_length=255)
    facebook_access_token_expires = models.PositiveIntegerField(blank=True, null=True)

    def image_name(self, filename):
        left_path, extension = filename.rsplit('.', 1)
        return 'volunteer/%s/%s/%s.%s' % (self.user.username,
                                          time(),
                                          self.user.username,
                                          extension)

    image = ImageField(upload_to=image_name, blank=True,
                       null=True, default=None)

    @classmethod
    def create(cls, user):
      return cls(user=user)

    @models.permalink
    def get_absolute_url(self):
      return ('slug', (self.user.username))

    def type(self):
      return "VOLUNTEER";

    def __unicode__(self):
        return self.user.first_name or self.user.username

class ProjectManager(models.Manager):
    use_for_related_fields = True

    def active(self):
        return self.get_query_set().filter(deleted=False)

    def published(self):
        return self.active().filter(published=True)


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
    date = models.DateTimeField(auto_now_add=True, blank=True)


class Recommendation(models.Model):
    project = models.ForeignKey(Project)
    sort = models.PositiveSmallIntegerField(_('Sort'),
            blank=True, null=True, default=None)
    state = models.ForeignKey(State, blank=True, null=True, default=None)
    city = models.ForeignKey(City, blank=True, null=True, default=None)
