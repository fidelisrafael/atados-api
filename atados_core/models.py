from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import post_save
from django.db.models import Count
from django.utils import timezone
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from import_export import resources, fields
from datetime import datetime
from atados import settings
from time import time

from pygeocoder import Geocoder

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
    active = models.BooleanField(_("City where Atados is present."), default=False)

    def __unicode__(self):
        return '%s, %s' % (self.name, self.state.code)

    class Meta:
        verbose_name = _('city')


class Address(models.Model):
    zipcode = models.CharField(_('Zip code'), max_length=10,
                               blank=True, null=True, default=None)
    addressline = models.CharField(_('Street'), max_length=200,
                                  blank=True, null=True, default=None)
    addressnumber = models.CharField(_('Address number'), max_length=10,
                                  blank=True, null=True, default=None)
    addressline2 = models.CharField(_('Apt, PO Box, block'), max_length=100,
                                  blank=True, null=True, default=None)
    neighborhood = models.CharField(_('Neighborhood'), max_length=50,
                                    blank=True, null=True, default=None)
    city = models.ForeignKey(City, verbose_name=_('City'), blank=False,
                             null=True, default=None)

    latitude = models.FloatField(blank=True, null=True, default=None)
    longitude = models.FloatField(blank=True, null=True, default=None)

    def __unicode__(self):
      return '%s, %s, %s - %s' % (self.addressline, self.addressnumber, self.addressline2, self.neighborhood)

def get_latitude_longitude(sender, instance, **kwargs):
  if instance.city and not instance.city.id == 0:
    if (not instance.latitude or not instance.longitude):
      try: 
        results = Geocoder.geocode(instance)
        instance.latitude = results[0].coordinates[0]
        instance.longitude = results[0].coordinates[1]
        instance.save()
      except Exception as e:
        pass

post_save.connect(get_latitude_longitude, sender=Address, dispatch_uid="get_latitude_longitude")

class Volunteer(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL)
  causes = models.ManyToManyField(Cause, blank=True, null=True)
  skills = models.ManyToManyField(Skill, blank=True, null=True)

  facebook_uid = models.CharField(blank=True, max_length=255)
  facebook_access_token = models.CharField(blank=True, max_length=255)
  facebook_access_token_expires = models.PositiveIntegerField(blank=True, null=True)

  def image_name(self, filename):
    left_path, extension = filename.rsplit('.', 1)
    return 'volunteer/%s/%s.%s' % (self.user.slug,
                                   self.user.slug,
                                   extension)

  image = models.ImageField(upload_to=image_name, blank=True,
                     null=True, default=None)

  @classmethod
  def create(cls, user):
    return cls(user=user)

  def get_type(self):
    return "VOLUNTEER"

  def get_full_name(self):
    name = self.user.first_name if self.user.first_name else ""
    name += self.user.last_name if self.user.last_name else ""
    return name

  def get_email(self):
    return self.user.email if self.user.email else None

  def get_phone(self):
    return self.user.phone if self.user.phone else None

  def get_apply(self):
    return Apply.objects.filter(volunteer=self)

  def get_image_url(self):
    return self.image.url if self.image else None

  def __unicode__(self):
    return self.user.first_name or self.user.slug


class NonprofitManager(models.Manager):
    #use_for_related_fields = True

    def active(self):
        return self.get_query_set().filter(deleted=False)

    def published(self):
        return self.active().filter(published=True)

class Nonprofit(models.Model):
    objects = NonprofitManager()
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    causes = models.ManyToManyField(Cause, blank=True, null=True)
    volunteers = models.ManyToManyField(Volunteer, blank=True, null=True)
    name = models.CharField(_('Name'), max_length=50)
    details = models.TextField(_('Details'), max_length=1024, blank=True,
                               null=True, default=None)
    description = models.TextField(_('Short description'), max_length=100,
                                   blank=True, null=True)
    website = models.URLField(blank=True, null=True, default=None)
    facebook_page = models.URLField(blank=True, null=True, default=None)
    google_page = models.URLField(blank=True, null=True, default=None)
    twitter_handle = models.CharField(max_length=51, blank=True, null=True, default=None)

    def image_name(self, filename):
        left_path, extension = filename.rsplit('.', 1)
        return 'nonprofit/%s.%s' % (self.user.slug, extension)

    def cover_name(self, filename):
        left_path, extension = filename.rsplit('.', 1)
        return 'nonprofit-cover/%s.%s' % (self.user.slug, extension)

    image = models.ImageField(upload_to=image_name, blank=True, null=True, default=None)
    cover = models.ImageField(upload_to=cover_name, blank=True, null=True, default=None)

    published = models.BooleanField(_("Published"), default=False)
    published_date = models.DateTimeField(_("Published date"), blank=True, null=True)
    deleted = models.BooleanField(_("Deleted"), default=False)
    deleted_date = models.DateTimeField(_("Deleted date"), blank=True, null=True)

    def delete(self, *args, **kwargs):
      self.deleted = True
      self.deleted_date = datetime.now()
      self.save()

    def get_type(self):
      return "NONPROFIT";

    def get_description(self):
      return self.description if self.description else Truncator(
              self.details).chars(100)

    def get_image_url(self):
      return self.image.url if self.image else None
    
    def get_cover_url(self):
      return self.cover.url if self.cover else None

    def get_volunteers(self):
      volunteers_from_projects = Volunteer.objects.filter(apply__project__nonprofit__id=self.id).count()
      volunteers_favorited = self.volunteers.count()
      return volunteers_from_projects + volunteers_favorited

    def __unicode__(self):
        return self.name

    def get_projects(self):
      return Project.objects.filter(nonprofit=self)

class ProjectManager(models.Manager):
    use_for_related_fields = True

    def active(self):
        return self.get_query_set().filter(deleted=False)

    def published(self):
        return self.active().filter(published=True)

# Cargo para um Ato pontual ou recorrente
class Role(models.Model):
    name = models.CharField(_('Role name'), max_length=50,
                            blank=True, null=True, default=None)
    prerequisites = models.TextField(_('Prerequisites'), max_length=1024,
                                    blank=True, null=True, default=None)
    details = models.TextField(_('Details'), max_length=1024, blank=True, null=True, default=None)
    vacancies = models.PositiveSmallIntegerField(_('Vacancies'),
                                    blank=True, null=True, default=None)
    start_date = models.DateTimeField(_("Start date"), blank=True, null=True)
    end_date = models.DateTimeField(_("End date"), blank=True, null=True)

class Project(models.Model):
    objects = ProjectManager()
    nonprofit = models.ForeignKey(Nonprofit)
    name = models.CharField(_('Project name'), max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    details = models.TextField(_('Details'), max_length=3000)
    description = models.TextField(_('Short description'), max_length=100, 
                                   blank=True, null=True)
    facebook_event = models.URLField(blank=True, null=True, default=None)
    responsible = models.CharField(_('Responsible name'), max_length=50,
                                   blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True)
    email = models.EmailField(_('E-mail'), blank=True, null=True)
    published = models.BooleanField(_("Published"), default=False)
    published_date = models.DateTimeField(_("Published date"), blank=True, null=True)
    closed = models.BooleanField(_("Closed"), default=False)
    closed_date = models.DateTimeField(_("Closed date"), blank=True, null=True)
    deleted = models.BooleanField(_("Deleted"), default=False)
    deleted_date = models.DateTimeField(_("Deleted date"), blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    address = models.OneToOneField(Address, blank=True, null=True)

    roles = models.ManyToManyField(Role, blank=True, null=True)
    skills = models.ManyToManyField(Skill)
    causes = models.ManyToManyField(Cause)

    legacy_nid = models.PositiveIntegerField(blank=True, null=True)

    def get_description(self):
        return self.description if self.description else Truncator(
                self.details).chars(75)
    
    def get_volunteers_count(self):
      return len(Apply.objects.filter(project=self))

    def get_volunteers(self):
      apply = Apply.objects.filter(project=self)
      return Volunteer.objects.filter(pk__in=[a.volunteer.pk for a in apply])

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.deleted_date = datetime.now()
        self.save()

    def image_name(self, filename):
        left_path, extension = filename.rsplit('.', 1)
        return 'project/%s/%s.%s' % (self.nonprofit.user.slug, self.slug, extension)

    image = models.ImageField(upload_to=image_name, blank=True,
                       null=True, default=None)

    def get_image_url(self):
      return self.image.url if self.image else None

    def __unicode__(self):
        return  '%s - %s' % (self.name, self.nonprofit.name)

    def get_project_type(self):
        return self.project_type


# Ato Recorrente
class Work(models.Model):
    project = models.OneToOneField(Project)
    availabilities = models.ManyToManyField(Availability)
    weekly_hours = models.PositiveSmallIntegerField(_('Weekly hours'),
                                        blank=True, null=True)
    can_be_done_remotely = models.BooleanField(_('This work can be done remotely.'))

# Ato Pontual
class Job(models.Model):
  project = models.OneToOneField(Project)
  start_date = models.DateTimeField(_("Start date"), blank=True, null=True);
  end_date = models.DateTimeField(_("End date"), blank=True, null=True)

class ApplyStatus(models.Model):
  name = models.CharField(_('name'), max_length=30)

  def __unicode__(self):
      return self.name

class Apply(models.Model):
  volunteer = models.ForeignKey(Volunteer)
  project = models.ForeignKey(Project)
  status = models.ForeignKey(ApplyStatus)
  date = models.DateTimeField(auto_now_add=True, blank=True)
  canceled = models.BooleanField(_("Canceled"), default=False)
  canceled_date = models.DateTimeField(_("Canceled date"), blank=True, null=True)

class Recommendation(models.Model):
  project = models.ForeignKey(Project)
  sort = models.PositiveSmallIntegerField(_('Sort'),
          blank=True, null=True, default=None)
  state = models.ForeignKey(State, blank=True, null=True, default=None)
  city = models.ForeignKey(City, blank=True, null=True, default=None)

class UserManager(BaseUserManager):

  def create_user(self, email, password=None, **extra_fields):
    now = timezone.now()
    if not email:
        raise ValueError('The given email address must be set')
    email = UserManager.normalize_email(email)
    user = self.model(email=email,
                      is_staff=False, is_active=True,
                      last_login=now, joined_date=now, **extra_fields)

    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, email, password, **extra_fields):
    user = self.create_user(email, password, **extra_fields)
    user.is_staff = True
    user.is_active = True
    user.is_superuser = True
    user.save()
    return user

class User(AbstractBaseUser):
  email = models.EmailField('Email', max_length=254, unique=True)
  first_name = models.CharField(_('first name'), max_length=50, blank=True)
  last_name = models.CharField(_('last name'), max_length=50, blank=True)
  slug = models.SlugField(_('Slug'), max_length=50, unique=True)

  is_staff = models.BooleanField(_('Staff'), default=False)
  is_active = models.BooleanField(_('Active'), default=True)
  is_email_verified = models.BooleanField(_('Email verified'), default=False)

  joined_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

  address = models.OneToOneField(Address, blank=True, null=True)
  phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True, default=None)

  legacy_uid = models.PositiveIntegerField(blank=True, null=True)

  objects = UserManager()
  USERNAME_FIELD = 'email'

  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')

  def get_full_name(self):
    full_name = '%s %s' % (self.first_name, self.last_name)
    return full_name.strip()

  def get_short_name():
    return self.first_name

  def email_user(self, subject, message, from_email=None):
    send_mail(subject, message, from_email, [self.email])

class VolunteerResource(resources.ModelResource):
  nome = fields.Field()
  email = fields.Field()
  telefone = fields.Field()

  class Meta:
    model = Volunteer
    fields = ()

  def dehydrate_nome(self, volunteer):
    return '%s %s' % (volunteer.user.first_name, volunteer.user.last_name)
  def dehydrate_email(self, volunteer):
    return volunteer.user.email
  def dehydrate_telefone(self, volunteer):
    return volunteer.user.phone

