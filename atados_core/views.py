import feedparser
import os

from atados_core.models import City, Suburb, Cause, Skill, Nonprofit, Project, Recommendation, Volunteer
from atados_core.permissions import IsOwnerOrReadOnly
from atados_core.serializers import NonprofitSerializer, VolunteerSerializer, UserSerializer, ProjectSerializer
from django import http
from django.contrib.auth.models import User
from django.core.cache import get_cache
from django.db.models import Q
from django.http import Http404, HttpResponseServerError
from django.template import RequestContext, TemplateDoesNotExist, loader
from django.utils import simplejson as json
from django.views.decorators.cache import cache_control, never_cache, cache_page
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import View, TemplateView
from django.views.generic.base import ContextMixin
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView
from rest_framework import generics, mixins, permissions, renderers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(('GET',))
def api_root(request, format=None):
  return Response({
    'users': reverse('user-list', request=request, format=format),
    'nonprofits': reverse('nonprofit-list', request=request, format=format),
    'projects': reverse('project-list', request=request, format=format)
  })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
  """
  This viewset automatically provides `list` and `detail` actions.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer

class NonprofitViewSet(viewsets.ReadOnlyModelViewSet):
  """
  This viewset automatically provides `list` and `detail` actions.
  """
  queryset = Nonprofit.objects.all()
  serializer_class = NonprofitSerializer

  def pre_save(self, obj):
    obj.user = self.request.user

class VolunteerViewSet(viewsets.ReadOnlyModelViewSet):
  """
  This viewset automatically provides `list` and `detail` actions.
  """
  queryset = Volunteer.objects.all()
  serializer_class = VolunteerSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
  """
  This viewset automatically provides `list` and `detail` actions.
  """
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer

@requires_csrf_token
def server_error(request, template_name='500.html'):
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseServerError('<h1>Server Error (500)</h1>')
    return HttpResponseServerError(template.render(RequestContext(request, {'request_path': request.path})))

def slug(request, *args, **kwargs):
    try:
        User.objects.get(username=kwargs['slug'])
        kwargs.update({
            'username': kwargs.pop('slug')
        })
        return VolunteerDetailsView.as_view()(request, *args, **kwargs)
    except User.DoesNotExist:
        try:
            Nonprofit.objects.get(slug=kwargs['slug'])
            kwargs.update({
                'nonprofit': kwargs.pop('slug')
            })
            from atados_nonprofit.views import NonprofitDetailsView
            return NonprofitDetailsView.as_view()(request, *args, **kwargs)
        except Nonprofit.DoesNotExist:
            raise Http404
