from haystack import indexes
from atados_core.models import Nonprofit, Project, Volunteer

class NonprofitIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)
  causes = indexes.MultiValueField(faceted=True)
  city = indexes.CharField(faceted=True)

  def prepare_city(self, obj):
    city = obj.user.address.city if obj.user.address else None
    return city.id if city else None

  def prepare_causes(self, obj):
    return [cause.id for cause in obj.causes.all()]

  def get_model(self):
    return Nonprofit

  def index_queryset(self, using=None):
    return self.get_model().objects.filter(deleted=False, published=True)

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)
  causes = indexes.MultiValueField(faceted=True)
  skills = indexes.MultiValueField(faceted=True)
  city = indexes.CharField(faceted=True)

  def prepare_causes(self, obj):
    return [cause.id for cause in obj.causes.all()]

  def prepare_skills(self, obj):
    return [skill.id for skill in obj.skills.all()]

  def prepare_city(self, obj):
    city = obj.address.city if obj.address else None
    return city.id if city else None

  def get_model(self):
    return Project

  def index_queryset(self, using=None):
    return self.get_model().objects.filter(closed=False, published=True, deleted=False)

class VolunteerIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)
  causes = indexes.MultiValueField(faceted=True)
  skills = indexes.MultiValueField(faceted=True)
  city = indexes.CharField(faceted=True)

  def prepare_causes(self, obj):
    return [cause.id for cause in obj.causes.all()]

  def prepare_skills(self, obj):
    return [skill.id for skill in obj.skills.all()]

  def prepare_city(self, obj):
    city = obj.user.address.city if obj.user.address else None
    return city.id if city else None

  def get_model(self):
    return Volunteer

  def prepare_published(self, obj):
    return True
