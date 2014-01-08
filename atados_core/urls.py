from django.conf import settings
from django.conf.urls import patterns, url, include

from atados_core import views
from atados_core.models import Project
from rest_framework.routers import DefaultRouter
from rest_framework.generics import ListAPIView
from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()
router.register(r'causes', views.CauseViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'states', views.StateViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'availabilities', views.AvailabilityViewSet)
router.register(r'nonprofit', views.NonprofitViewSet)
router.register(r'project', views.ProjectViewSet)
router.register(r'volunteers', views.VolunteerViewSet)

urlpatterns = patterns('atados_core.views',
  url(r'v1/oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
  url(r'v1/facebook/', 'facebook_auth'),
  url(r'v1/current_user/', 'current_user'),
  url(r'v1/password_reset/', 'password_reset'),
  url(r'v1/change_password/', 'change_password'),
  url(r'v1/logout/', 'logout'),

  url(r'v1/create/volunteer/', 'create_volunteer'),
  url(r'v1/create/nonprofit/', 'create_nonprofit'),

  url(r'v1/check_slug/', 'check_slug'),
  url(r'v1/check_project_slug/', 'check_project_slug'),
  url(r'v1/check_email/', 'check_email'),

  url(r'v1/upload_volunteer_image/', 'upload_volunteer_image'),
  url(r'v1/upload_nonprofit_profile_image/', 'upload_nonprofit_profile_image'),
  url(r'v1/upload_nonprofit_cover_image/', 'upload_nonprofit_cover_image'),

  url(r'v1/set_volunteer_to_nonprofit/', 'set_volunteer_to_nonprofit'),
  url(r'v1/is_volunteer_to_nonprofit/', 'is_volunteer_to_nonprofit'),
  url(r'v1/change_volunteer_status/', 'change_volunteer_status'),

  url(r'v1/numbers/', 'numbers'),

  url(r'v1/projects/', views.ProjectList.as_view()),
  url(r'v1/nonprofits/', views.NonprofitList.as_view()),
  url(r'v1/project/(?P<project_slug>[\w-]+)/volunteers/', views.VolunteerProjectList.as_view()),
  url(r'v1/project/(?P<project_slug>[\w-]+)/clone/', 'clone_project'),
  url(r'v1/project/(?P<project_slug>[\w-]+)/export/', 'export_project_csv'),
)

urlpatterns += patterns('',
  url(r'^v1/api/', include('rest_framework.urls', namespace='rest_framework')),
  url(r'^v1/', include(router.urls)),
)
