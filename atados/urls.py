from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, url, include

from atados_core import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

admin.autodiscover()

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'volunteers', views.VolunteerViewSet)
router.register(r'nonprofits', views.NonprofitViewSet)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),

    # Authentication URLs
    url(r'^current-user/', 'atados_core.views.current_user'),
    url(r'^login/', 'atados_core.views.login'),
    # url(r'^login/facebook', 'atados_core.views.login_facebook'),
    url(r'^logout/', 'atados_core.views.logout'),

    url(r'^v1/', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
)
