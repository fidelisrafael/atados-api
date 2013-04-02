import datetime
from django.db.models import signals
from haystack import indexes, site
from atados.project.models import (Project, ProjectDonation, ProjectWork, ProjectJob)


class ProjectIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    causes = indexes.MultiValueField(faceted=True)
    state = indexes.CharField(model_attr='state', faceted=True, null=True)
    city = indexes.CharField(model_attr='city', faceted=True, null=True)
    suburb = indexes.CharField(model_attr='suburb', faceted=True, null=True)

    def prepare_causes(self, obj):
        return [cause.id for cause in obj.causes.all()]


class SkillsIndexMixin(object):
    skills = indexes.MultiValueField(faceted=True)

    def prepare_skills(self, obj):
        return [skill.id for skill in obj.skills.all()]


class ProjectDonationIndex(ProjectIndex):
    pass
    
class ProjectWorkIndex(ProjectIndex, SkillsIndexMixin):
    pass

class ProjectJobIndex(ProjectIndex, SkillsIndexMixin):
    pass

site.register(ProjectJob, ProjectJobIndex)
site.register(ProjectWork, ProjectWorkIndex)
site.register(ProjectDonation, ProjectDonationIndex)
