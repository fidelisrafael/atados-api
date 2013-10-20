from django.conf import settings
from django.conf.urls import patterns, url, include

from atados_core import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'volunteers', views.VolunteerViewSet)
router.register(r'nonprofits', views.NonprofitViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'causes', views.CauseViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'addresses', views.AddressViewSet)
router.register(r'states', views.StateViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'suburbs', views.SuburbViewSet)
router.register(r'availabilities', views.AvailabilityViewSet)

urlpatterns = patterns('atados_core.views',
  url(r'^v1/oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
  url(r'v1/facebook', 'facebook_auth'),
  url(r'^v1/current_user/', 'current_user'),
  url(r'^v1/check_username/', 'check_username'),
  url(r'^v1/check_slug/', 'check_slug'),
  url(r'^v1/check_email/', 'check_email'),
  url(r'^v1/password_reset/', 'password_reset'),
  url(r'^v1/logout/', 'logout'),
  url(r'^v1/upload_volunteer_image/', 'upload_volunteer_image'),
  url(r'^v1/create/volunteer/', 'create_volunteer'),
  url(r'^v1/create/nonprofit/', 'create_nonprofit'),
)

urlpatterns += patterns('',
  url(r'^v1/api/', include('rest_framework.urls', namespace='rest_framework')),
  url(r'^v1/', include(router.urls)),
)
