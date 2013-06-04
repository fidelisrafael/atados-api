import datetime
from django.db.models import signals
from haystack import indexes
from atados_project.models import Project


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    causes = indexes.MultiValueField(faceted=True)
    has_image = indexes.BooleanField()
    published = indexes.BooleanField(model_attr='published')

    def prepare_causes(self, obj):
        return [cause.id for cause in obj.causes.all()]

    def prepare_has_image(self, obj):
        return True if obj.image else False

    def get_model(self):
        return Project
