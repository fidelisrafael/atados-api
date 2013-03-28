import datetime
from django.db.models import signals
from haystack import indexes, site
from atados.project.models import (ProjectDonation, ProjectWork, ProjectJob)


class ProjectJobIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)

class ProjectWorkIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)

class ProjectDonationIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)

site.register(ProjectJob, ProjectJobIndex)
site.register(ProjectWork, ProjectWorkIndex)
site.register(ProjectDonation, ProjectDonationIndex)
