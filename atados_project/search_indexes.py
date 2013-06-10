import datetime
from django.db.models import signals
from haystack import indexes
from atados_core.models import Address
from atados_project.models import Project


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
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
        if hasattr(obj, 'work'):
            return [skill.id for skill in obj.work.skills.all()]
        return []

    def get_address(self, obj):
        if hasattr(obj, 'work') and obj.work.address:
            return obj.work.address
        if hasattr(obj, 'donation') and obj.donation.delivery:
            return obj.work.address
        return Address()

    def prepare_state(self, obj):
        estate = self.get_address(obj).state
        return estate.id if estate else None

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

    def get_model(self):
        return Project
