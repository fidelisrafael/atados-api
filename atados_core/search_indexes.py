import datetime
from django.db.models import signals
from haystack import indexes
from atados_core.models import Address, Nonprofit, Project, Volunteer

class NonprofitIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)
  causes = indexes.MultiValueField(faceted=True)
  skills = indexes.MultiValueField(faceted=True)
  state = indexes.CharField(faceted=True)
  city = indexes.CharField(faceted=True)
  suburb = indexes.CharField(faceted=True)
  availabilities = indexes.MultiValueField(faceted=True)
  has_image = indexes.BooleanField()
  published = indexes.BooleanField(model_attr='published')

  def prepare_causes(self, obj):
    return [cause.id for cause in obj.causes.all()]

  def prepare_skills(self, obj):
    return []

  def prepare_state(self, obj):
    return obj.address.suburb.city.state.id if obj.address and obj.address.suburb.city.state else None

  def prepare_city(self, obj):
    return obj.address.suburb.city.id if obj.address and obj.address.suburb.city else None

  def prepare_suburb(self, obj):
    return obj.address.suburb.id if obj.address and obj.address.suburb else None

  def prepare_availabilities(self, obj):
    return []

  def prepare_has_image(self, obj):
    return True if obj.image else False

  def get_model(self):
    return Nonprofit

  def index_queryset(self, using=None):
    return self.get_model().objects.filter(deleted=False)

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)
  causes = indexes.MultiValueField(faceted=True)
  skills = indexes.MultiValueField(faceted=True)
  state = indexes.CharField(faceted=True)
  city = indexes.CharField(faceted=True)
  suburb = indexes.CharField(faceted=True)
  availabilities = indexes.MultiValueField(faceted=True)
  has_image = indexes.BooleanField()
  published = indexes.BooleanField()

  def prepare_causes(self, obj):
    return [cause.id for cause in obj.causes.all()]

  def prepare_skills(self, obj):
    if hasattr(obj, 'work'):
      return [skill.id for skill in obj.work.skills.all()]
    return []

  def get_address(self, obj):
    if hasattr(obj, 'work') and obj.work.address:
      return obj.work.address
    if hasattr(obj, 'donation') and obj.donation.delivery:
      return obj.donation.delivery
    return Address()

  def prepare_state(self, obj):
    state = self.get_address(obj).city.state if self.get_address(obj).city else None
    return state.id if state else None

  def prepare_city(self, obj):
    city = self.get_address(obj).city
    return city.id if city else None

  def prepare_suburb(self, obj):
    suburb = self.get_address(obj).suburb
    return suburb.id if suburb else None

  def prepare_availabilities(self, obj):
    if hasattr(obj, 'work'):
      return [availability.id for availability in obj.work.availabilities.all()]
    return []

  def prepare_has_image(self, obj):
    return True if obj.image else False

  def prepare_published(self, obj):
    return True if obj.published and obj.nonprofit.published else False

  def get_model(self):
    return Project

class VolunteerIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)
  causes = indexes.MultiValueField(faceted=True)
  skills = indexes.MultiValueField(faceted=True)
  state = indexes.CharField(faceted=True)
  city = indexes.CharField(faceted=True)
  suburb = indexes.CharField(faceted=True)
  availabilities = indexes.MultiValueField(faceted=True)
  has_image = indexes.BooleanField()
  published = indexes.BooleanField()

  def prepare_causes(self, obj):
    return [cause.id for cause in obj.causes.all()]

  def prepare_skills(self, obj):
    return [skill.id for skill in obj.skills.all()]

  def get_address(self, obj):
    if hasattr(obj, 'work') and obj.work.address:
      return obj.work.address
    if hasattr(obj, 'donation') and obj.donation.delivery:
      return obj.work.address
    return Address()

  def prepare_availabilities(self, obj):
    return []

  def prepare_has_image(self, obj):
    return True if obj.image else False

  def get_model(self):
    return Volunteer

  def prepare_published(self, obj):
    return True
