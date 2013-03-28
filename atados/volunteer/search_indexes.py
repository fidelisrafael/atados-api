import datetime
from haystack import indexes
from atados.volunteer.models import Volunteer


class ProjectIndex(indexes.RealTimeSearchIndex, indexes.SearchIndex):
    text = indexes.CharField(document=True, model_attr='user')

    def get_model(self):
        return Volunteer
