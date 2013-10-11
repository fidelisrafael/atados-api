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
    url(r'^current-user/', 'current_user'),
    url(r'^logout/', 'logout'),
    url(r'^v1/', include(router.urls)),
)

urlpatterns += patterns('',
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token')
)
