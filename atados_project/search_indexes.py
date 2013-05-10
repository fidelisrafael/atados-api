import datetime
from django.db.models import signals
from haystack import indexes
from atados_project.models import Project


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    causes = indexes.MultiValueField(faceted=True)
    state = indexes.CharField(model_attr='state', faceted=True, null=True)
    city = indexes.CharField(model_attr='city', faceted=True, null=True)
    suburb = indexes.CharField(model_attr='suburb', faceted=True, null=True)

    def prepare_causes(self, obj):
        return [cause.id for cause in obj.causes.all()]

    def get_model(self):
        return Project
