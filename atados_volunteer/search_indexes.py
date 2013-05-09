import datetime
from haystack import indexes, site
from atados_volunteer.models import Volunteer


class VolunteerIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)

site.register(Volunteer, VolunteerIndex)
