import datetime
from haystack import indexes, site
from atados.nonprofit.models import Nonprofit


class NonprofitIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)

site.register(Nonprofit, NonprofitIndex)
