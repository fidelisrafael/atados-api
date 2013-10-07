from atados_core import views
from atados_core.views import (NonprofitViewSet,
                               UserViewSet,
                               VolunteerViewSet,
                               ProjectViewSet)
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, RedirectView
from rest_framework.urlpatterns import format_suffix_patterns

user_list = UserViewSet.as_view({
  'get': 'list'
})
user_detail = UserViewSet.as_view({
  'get': 'retrieve'
})
volunteer_list = VolunteerViewSet.as_view({
  'get': 'list'
})
volunteer_detail = VolunteerViewSet.as_view({
  'get': 'retrieve'
})
nonprofit_list = NonprofitViewSet.as_view({
  'get': 'list',
  'post': 'create'
})
nonprofit_detail = NonprofitViewSet.as_view({
  'get': 'retrieve',
  'put': 'update',
  'patch': 'partial_update',
  'delete': 'destroy'
})
project_list = ProjectViewSet.as_view({
  'get': 'list',
  'post': 'create'
})
project_detail = ProjectViewSet.as_view({
  'get': 'retrieve',
  'put': 'update',
  'patch': 'partial_update',
  'delete': 'destroy'
})

urlpatterns = patterns('',
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    url(r'^nonprofits/$', nonprofit_list, name='nonprofit-list'),
    url(r'^nonprofits/(?P<pk>[0-9]+)/$', nonprofit_detail, name='nonprofit-detail')

)

urlpatterns = format_suffix_patterns(urlpatterns)
