import datetime
from haystack import indexes
from atados_volunteer.models import Volunteer


class VolunteerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Volunteer
