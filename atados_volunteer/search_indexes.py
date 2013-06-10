import datetime
from haystack import indexes
from atados_volunteer.models import Volunteer


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
