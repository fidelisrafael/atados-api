import datetime
from haystack import indexes
from atados_nonprofit.models import Nonprofit


class NonprofitIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Nonprofit
