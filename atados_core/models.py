# -*- coding: utf-8 -*- 

import pytz
import random
import hashlib

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from django.db import models
from django.db.models import Q 

from django.utils import timezone
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from import_export import resources, fields
from datetime import datetime
from atados import settings
from unidecode import unidecode


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

  class Meta:
    verbose_name = _('availability')

class Cause(models.Model):
    name = models.CharField(_('name'), max_length=100)

    def __unicode__(self):
      return self.name

    class Meta:
      verbose_name = _('cause')
      verbose_name_plural = _('causes')

class Skill(models.Model):
    name = models.CharField(_('name'), max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
      verbose_name = _('skill')

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
        verbose_name_plural = _('cities')

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
    city = models.ForeignKey(City, verbose_name=_('City'), blank=True,
                             null=True, default=None)

    latitude = models.FloatField(blank=False, null=False, default=0.0)
    longitude = models.FloatField(blank=False, null=False, default=0.0)

    modified_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
      if self.city and not self.city.id == 0:
        try:
          results = Geocoder.geocode(self)
          self.latitude = results[0].coordinates[0]
          self.longitude = results[0].coordinates[1]
        except Exception as e:
          print e

      self.modified_date = datetime.utcnow().replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
      return super(Address, self).save(*args, **kwargs)

    def __unicode__(self):
      address = '';
      if self.addressline:
        address = self.addressline
      if self.addressnumber:
        address = '%s, %s' % (address, self.addressnumber)
      if self.addressline2:
        address = '%s, %s' % (address, self.addressline2)
      if self.neighborhood:
        address = '%s, %s' % (address, self.neighborhood)
      if self.city:
        if address == '':
          address = '%s, %s' % (self.city.name, self.city.state.code)
        else:
          address = '%s - %s, %s' % (address, self.city.name, self.city.state.code)
      return address

    def get_city_state(self):
      if self.city:
        if self.city.id == 0: # Trabalho a Distancia
          return self.city.name
        return "%s, %s" % (self.city.name, self.city.state.code)
      else:
        return ""

    class Meta:
      verbose_name = _('address')

class Company(models.Model):
  name = models.CharField(_('name'), max_length=300)
  address = models.OneToOneField(Address, blank=True, null=True)

  def __unicode__(self):
    return self.name

def volunteer_image_name(self, filename):
    left_path, extension = filename.rsplit('.', 1)
    return 'volunteer/%s/%s.%s' % (self.user.slug,
                                   self.user.slug,
                                   extension)
class Volunteer(models.Model):

  class Meta:
    verbose_name = _('volunteer')
    verbose_name_plural = _('volunteers')

  user = models.OneToOneField(settings.AUTH_USER_MODEL)
  causes = models.ManyToManyField(Cause, blank=True, null=True)
  skills = models.ManyToManyField(Skill, blank=True, null=True)

  facebook_uid = models.CharField(blank=True, max_length=255)
  facebook_access_token = models.CharField(blank=True, max_length=255)
  facebook_access_token_expires = models.PositiveIntegerField(blank=True, null=True)

  birthDate = models.DateField(null=True, blank=True, default=None)

  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)

  image = models.ImageField(upload_to=volunteer_image_name, blank=True,
                   null=True, default=None)

  def image_name(self, filename):
    return volunteer_image_name(self, filename);

  @classmethod
  def create(cls, user):
    return cls(user=user)

  def get_type(self):
    return "VOLUNTEER"

  def get_full_name(self):
    return self.user.name

  def get_email(self):
    return self.user.email if self.user.email else None

  def get_phone(self):
    return self.user.phone if self.user.phone else None

  def get_apply(self):
    return Apply.objects.filter(volunteer=self)

  def get_image_url(self):
    return self.image.url if self.image else 'https://s3-sa-east-1.amazonaws.com/atadosapp/volunteer/default_profile.jpg'

  def get_projects(self):
    return Project.objects.filter(id__in=Apply.objects.filter(volunteer_id=self.id, canceled=False).values_list('project', flat=True))

  def get_nonprofits(self):
    return Nonprofit.objects.filter(volunteers__in=[self]) | Nonprofit.objects.filter(id__in=self.get_projects().values_list('nonprofit', flat=True))

  def save(self, *args, **kwargs):
    self.modified_date = datetime.utcnow().replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
    return super(Volunteer, self).save(*args, **kwargs)

  def __unicode__(self):
    return self.user.name

  
def nonprofit_image_name(self, filename):
        left_path, extension = filename.rsplit('.', 1)
        return 'nonprofit/%s.%s' % (self.user.slug, extension)

def nonprofit_cover_name(self, filename):
        left_path, extension = filename.rsplit('.', 1)
        return 'nonprofit-cover/%s.%s' % (self.user.slug, extension)


class Nonprofit(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    causes = models.ManyToManyField(Cause, blank=True, null=True)
    volunteers = models.ManyToManyField(Volunteer, blank=True, null=True)
    name = models.CharField(_('Name'), max_length=150)

    def ascii_name(self):
      return unidecode(self.name)

    details = models.TextField(_('Details'), max_length=2048, blank=True,
                               null=True, default=None)
    description = models.TextField(_('Short description'), max_length=160,
                                   blank=True, null=True)
    website = models.URLField(blank=True, null=True, default=None)
    facebook_page = models.URLField(blank=True, null=True, default=None)
    google_page = models.URLField(blank=True, null=True, default=None)
    twitter_handle = models.URLField(blank=True, null=True, default=None)

    companies = models.ManyToManyField(Company, blank=True, null=True)
    
    def image_tag(self):
        return u'<img src="%s" />' % self.image.url
    image_tag.short_description = 'Logo 200x200'
    image_tag.allow_tags = True

    def cover_tag(self):
      return u'<img src="%s" />' % self.cover.url
    cover_tag.short_description = 'Cover 1450x340'
    cover_tag.allow_tags = True

    def image_name(self, filename):
      return nonprofit_image_name(self, filename);

    image = models.ImageField(_("Logo 200x200"), upload_to=nonprofit_image_name, blank=True, null=True, default=None)
    cover = models.ImageField(_("Cover 1450x340"),upload_to=nonprofit_cover_name, blank=True, null=True, default=None)

    highlighted = models.BooleanField(_("Highlighted"), default=False, blank=False)
    published = models.BooleanField(_("Published"), default=False)
    published_date = models.DateTimeField(_("Published date"), blank=True, null=True)
    deleted = models.BooleanField(_("Deleted"), default=False)
    deleted_date = models.DateTimeField(_("Deleted date"), blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

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
      return self.image.url if self.image else "https://s3-sa-east-1.amazonaws.com/atadosapp/nonprofit/default_nonprofit.png"
    
    def get_cover_url(self):
      return self.cover.url if self.cover else "https://s3-sa-east-1.amazonaws.com/atadosapp/nonprofit-cover/default_nonprofit.png"

    def get_volunteers(self):
      return Volunteer.objects.filter(
        Q(id__in=self.volunteers.all().values_list('id', flat=True)) |
        Q(apply__project__nonprofit__id=self.id)).distinct()

    def get_volunteers_numbers(self):
      return Volunteer.objects.filter(
        Q(id__in=self.volunteers.all().values_list('id', flat=True)) |
        Q(apply__project__nonprofit__id=self.id)).distinct().count

    def __unicode__(self):
        return self.name

    def get_projects(self):
      return Project.objects.filter(nonprofit=self, deleted=False)

    def get_address(self):
      return self.user.address

    def save(self, *args, **kwargs):
      if self.pk is not None:
        orig = Nonprofit.objects.get(pk=self.pk)
        if not orig.published and self.published:
          self.published_date = datetime.utcnow().replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
          # Sending welcome email on nonprofit signup
          plaintext = get_template('email/nonprofitApproved.txt')
          htmly     = get_template('email/nonprofitApproved.html')
          d = Context()
          subject, from_email, to = 'Cadastro no Atados realizado com sucesso!', 'contato@atados.com.br', self.user.email
          text_content = plaintext.render(d)
          html_content = htmly.render(d)
          msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
          msg.attach_alternative(html_content, "text/html")
          msg.send()

      self.modified_date = datetime.utcnow().replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
      return super(Nonprofit, self).save(*args, **kwargs)

    class Meta:
      verbose_name = _('nonprofit')



# Cargo para um Ato pontual ou recorrente
class Role(models.Model):
    name = models.CharField(_('Role name'), max_length=50,
                            blank=True, null=True, default=None)
    prerequisites = models.TextField(_('Prerequisites'), max_length=1024,
                                    blank=True, null=True, default=None)
    details = models.TextField(_('Details'), max_length=1024, blank=True, null=True, default=None)
    vacancies = models.PositiveSmallIntegerField(_('Vacancies'),
                                    blank=True, null=True, default=None)
    class Meta:
      verbose_name = _('role')
      verbose_name_plural = _('roles')

    def __unicode__(self):
      return  '%s - %s - %s (%s vagas)' % (self.name, self.details, self.prerequisites, self.vacancies)


def project_image_name(self, filename):
    left_path, extension = filename.rsplit('.', 1)
    return 'project/%s/%s.%s' % (self.nonprofit.user.slug, self.slug, extension)

class Project(models.Model):
  nonprofit = models.ForeignKey(Nonprofit)
  name = models.CharField(_('Project name'), max_length=50)

  def ascii_name(self):
    return unidecode(self.name)

  slug = models.SlugField(max_length=100, unique=True)
  details = models.TextField(_('Details'), max_length=2048)
  description = models.TextField(_('Short description'), max_length=160,
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

  highlighted = models.BooleanField(_("Highlighted"), default=False, blank=False)

  roles = models.ManyToManyField(Role, blank=True, null=True)

  skills = models.ManyToManyField(Skill)
  causes = models.ManyToManyField(Cause)

  legacy_nid = models.PositiveIntegerField(blank=True, null=True)

  companies = models.ManyToManyField(Company, blank=True, null=True)

  
  def image_tag(self):
        return u'<img src="%s" />' % self.image.url
  image_tag.short_description = 'Image 350x260'
  image_tag.allow_tags = True


  image = models.ImageField(_('Image 350x260'), upload_to=project_image_name, blank=True,
                     null=True, default=None)

  def get_volunteers(self):
    apply = Apply.objects.filter(project=self, canceled=False)
    return Volunteer.objects.filter(pk__in=[a.volunteer.pk for a in apply])

  def get_volunteers_numbers(self):
    return Apply.objects.filter(project=self, canceled=False).count

  def delete(self, *args, **kwargs):
      self.deleted = True
      self.deleted_date = datetime.now()
      self.save()

  def save(self, *args, **kwargs):
    if self.pk is not None:
        orig = Project.objects.get(pk=self.pk)
        if not orig.published and self.published:
          self.published_date = datetime.utcnow().replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
          # Sending welcome email on project creation
          plaintext = get_template('email/projectApproved.txt')
          htmly     = get_template('email/projectApproved.html')
          d = Context()
          subject, from_email, to = u"Seu ato já está no ar.", 'contato@atados.com.br', self.email
          text_content = plaintext.render(d)
          html_content = htmly.render(d)
          msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
          msg.attach_alternative(html_content, "text/html")
          msg.send()

    self.modified_date = datetime.utcnow().replace(tzinfo=pytz.timezone("America/Sao_Paulo"))

    # If there is no description, take 100 chars from the details
    if not self.description and len(self.details) > 100:
      self.description = self.details[0:100]

    return super(Project, self).save(*args, **kwargs)

  def get_image_url(self):
    return self.image.url if self.image else 'https://s3-sa-east-1.amazonaws.com/atadosapp/project/default_project.jpg'

  def __unicode__(self):
      return  '%s - %s' % (self.name, self.nonprofit.name)

  class Meta:
    verbose_name = _('project')
    verbose_name_plural = _('projects')

class AddressProject(Project):
  class Meta:
    proxy = True
  
# Ato Recorrente
class Work(models.Model):
  project = models.OneToOneField(Project, blank=True, null=True)
  availabilities = models.ManyToManyField(Availability)
  weekly_hours = models.PositiveSmallIntegerField(_('Weekly hours'),
                                      blank=True, null=True)
  can_be_done_remotely = models.BooleanField(_('This work can be done remotely.'), default=False)

  def __unicode__(self):
    return "%s horas por semana" % (self.weekly_hours)

  class Meta:
    verbose_name = _('work')
    verbose_name_plural = _('works')

# Ato Pontual
class Job(models.Model):
  project = models.OneToOneField(Project, blank=True, null=True)
  start_date = models.DateTimeField(_("Start date"), blank=True, null=True);
  end_date = models.DateTimeField(_("End date"), blank=True, null=True)

  def __unicode__(self):
    return "%s - %s" % (self.start_date, self.end_date)

  class Meta:
    verbose_name = _('Job')
    verbose_name_plural = _('Jobs')

class ApplyStatus(models.Model):
  name = models.CharField(_('name'), max_length=30)

  def __unicode__(self):
      return self.name

  class Meta:
    verbose_name = _('apply status')

class Apply(models.Model):
  volunteer = models.ForeignKey(Volunteer)
  project = models.ForeignKey(Project)
  status = models.ForeignKey(ApplyStatus)
  date = models.DateTimeField(auto_now_add=True, blank=True) # created date
  canceled = models.BooleanField(_("Canceled"), default=False)
  canceled_date = models.DateTimeField(_("Canceled date"), blank=True, null=True)

  def save(self, *args, **kwargs):
    if self.canceled:
      self.canceled_date = datetime.now().replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
    else:
      self.canceled_date = None
    return super(Apply, self).save(*args, **kwargs)

  def __unicode__(self):
    return "[%s] %s - %s" % (self.canceled, self.volunteer.user.name, self.project.name)

  class Meta:
    verbose_name = _('apply')
    verbose_name_plural = _('applies')

class Recommendation(models.Model):
  project = models.ForeignKey(Project)
  sort = models.PositiveSmallIntegerField(_('Sort'),
          blank=True, null=True, default=None)
  state = models.ForeignKey(State, blank=True, null=True, default=None)
  city = models.ForeignKey(City, blank=True, null=True, default=None)

  class Meta:
    verbose_name = _('recommendation')

def random_token(extra=None, hash_func=hashlib.sha256):
    if extra is None:
        extra = []
    bits = extra + [str(random.SystemRandom().getrandbits(512))]
    return hash_func("".join(bits).encode('utf-8')).hexdigest()

class UserManager(BaseUserManager):

  def create_user(self, email, password=None, **extra_fields):
    now = timezone.now()
    if not email:
        raise ValueError('The given email address must be set')
    email = UserManager.normalize_email(email)
    token = random_token([email])
    user = self.model(email=email, token=token,
                      is_staff=False, is_active=True,
                      last_login=now, joined_date=now, **extra_fields)

    site = extra_fields.get('site', 'https://www.atados.com.br')
    plaintext = get_template('email/emailVerification.txt')
    htmly     = get_template('email/emailVerification.html')
    subject   = u'Confirme seu email do Atados.'
    d = Context({ 'token': token , 'site': site})
    from_email, to = 'contato@atados.com.br', email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

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
  name = models.CharField(_('Name'), max_length=200, blank=True)
  slug = models.SlugField(_('Slug'), max_length=100, unique=True)

  is_staff = models.BooleanField(_('Staff'), default=False)
  is_active = models.BooleanField(_('Active'), default=True)
  is_email_verified = models.BooleanField(_('Email verified'), default=False)

  joined_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

  address = models.OneToOneField(Address, blank=True, null=True)
  hidden_address = models.BooleanField(_("Endereco escondido."), default=False)

  company = models.ForeignKey(Company, blank=True, null=True)

  site = models.URLField(blank=True, null=True, default=None)

  phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True, default=None)

  legacy_uid = models.PositiveIntegerField(blank=True, null=True)
  token = models.CharField(verbose_name=_('token'), max_length=64, unique=True, null=True, default=None)

  objects = UserManager()
  USERNAME_FIELD = 'email'

  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')

  def email_user(self, subject, message, from_email=None):
    send_mail(subject, message, from_email, [self.email])

  def get_short_name(self):
    return self.name

  def save(self, *args, **kwargs):
    self.modified_date = datetime.utcnow().replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
    return super(User, self).save(*args, **kwargs)

  def get_address(self):
    if self.hidden_address:
      try:
        return Address.objects.filter(id__in=[1, 2, 3], city__id=self.address.city.id)[0]
      except:
        return None


  def has_module_perms(self, app_label):
    # Handle whether the user has permissions to view the app `app_label`?"
    return True

  def has_perm(self, perm, obj=None):
    # Handle whether the user has a specific permission?"
    return True

class Comment(models.Model):
  project = models.ForeignKey(Project, null=False)
  user = models.ForeignKey(User, null=False) 
  comment = models.TextField()
  created_date = models.DateTimeField(auto_now_add=True)
  deleted = models.BooleanField(_("Deleted"), default=False)
  deleted_date = models.DateTimeField(_("Deleted date"), blank=True, null=True)

  def delete(self, *args, **kwargs):
    self.deleted = True
    self.deleted_date = datetime.utcnow().replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
    self.save()

  def __unicode__(self):
    return "(%s) %s: %s" % (self.project.name, self.user.email, self.comment)

class VolunteerResource(resources.ModelResource):
  nome = fields.Field()
  email = fields.Field()
  telefone = fields.Field()

  class Meta:
    model = Volunteer
    fields = ()

  def dehydrate_nome(self, volunteer):
    return volunteer.user.name
  def dehydrate_email(self, volunteer):
    return volunteer.user.email
  def dehydrate_telefone(self, volunteer):
    return volunteer.user.phone

