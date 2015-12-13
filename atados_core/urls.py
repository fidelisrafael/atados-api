# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from atados_core import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'causes', views.CauseViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'states', views.StateViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'nonprofit', views.NonprofitViewSet)
router.register(r'project', views.ProjectViewSet)
router.register(r'jobs', views.JobViewSet)
router.register(r'works', views.WorkViewSet)
router.register(r'volunteers', views.VolunteerViewSet)
router.register(r'volunteers_public', views.VolunteerPublicViewSet)

urlpatterns = patterns('atados_core.views',
  url(r'^v1/api/', include('rest_framework.urls', namespace='rest_framework')),
  url(r'^v1/', include(router.urls)),

  url(r'v1/oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
  url(r'v1/facebook/', 'facebook_auth'),
  url(r'v1/current_user/', 'current_user'),
  url(r'v1/password_reset/', 'password_reset'),
  url(r'v1/change_password/', 'change_password'),
  url(r'v1/logout/', 'logout'),

  url(r'v1/create/volunteer/', 'create_volunteer'),
  url(r'v1/create/nonprofit/', 'create_nonprofit'),
  url(r'v1/create/project/', 'create_project'),
  url(r'v1/save/project', 'save_project'),
  url(r'v1/open/project', 'open_project'),
  url(r'v1/close/project', 'close_project'),

  url(r'v1/check_slug/', 'check_slug'),
  url(r'v1/generate_slug/(?P<nonprofit_name>[\wi\ ]+)/', 'generate_slug'),
  url(r'v1/check_email/', 'check_email'),
  url(r'v1/confirm_email/', 'confirm_email'),

  url(r'v1/legacy_to_slug/(?P<type>[\w-]+)/', 'legacy_to_slug'),
  url(r'v1/slug_role/', 'slug_role'),

  url(r'v1/upload_volunteer_image/', 'upload_volunteer_image'),
  url(r'v1/upload_project_image/', 'upload_project_image'),
  url(r'v1/upload_nonprofit_profile_image/', 'upload_nonprofit_profile_image'),
  url(r'v1/upload_nonprofit_cover_image/', 'upload_nonprofit_cover_image'),

  url(r'v1/set_volunteer_to_nonprofit/', 'set_volunteer_to_nonprofit'),
  url(r'v1/is_volunteer_to_nonprofit/', 'is_volunteer_to_nonprofit'),
  url(r'v1/change_volunteer_status/', 'change_volunteer_status'),
  url(r'v1/apply_volunteer_to_project/', 'apply_volunteer_to_project'),
  url(r'v1/has_volunteer_applied/', 'has_volunteer_applied'),

  url(r'v1/numbers/', 'numbers'),
  url(r'v1/startup/', 'startup'),

  url(r'v1/projects/', views.ProjectList.as_view()), # Powers search and explore view
  url(r'v1/map/projects/', views.ProjectMapList.as_view()),
  url(r'v1/nonprofits/', views.NonprofitList.as_view()), # Powers search and explore view
  url(r'v1/map/nonprofits/', views.NonprofitMapList.as_view()),
  url(r'v1/applies/', views.ApplyList.as_view()),
  url(r'v1/project/(?P<project_slug>[\w-]+)/volunteers/', views.VolunteerProjectList.as_view()),
  url(r'v1/project/(?P<project_slug>[\w-]+)/clone/', 'clone_project'),
  url(r'v1/project/(?P<project_slug>[\w-]+)/export/', 'export_project_csv'),

  url(r'v1/dashboard/applies/', 'applies'),

  url(r'v1/add_to_newsletter/', 'add_to_newsletter'),

  url(r'v1/contribute/', 'contribute'),
  url(r'v1/contributions/', 'contributions'),
)
