import datetime
from haystack import indexes
from atados_nonprofit.models import Nonprofit


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
        return obj.address.state.id if obj.address and obj.address.state else None

    def prepare_city(self, obj):
        return obj.address.city.id if obj.address and obj.address.city else None

    def prepare_suburb(self, obj):
        return obj.address.suburb.id if obj.address and obj.address.suburb else None

    def prepare_availabilities(self, obj):
        return []

    def prepare_has_image(self, obj):
        return True if obj.image else False

    def get_model(self):
        return Nonprofit
