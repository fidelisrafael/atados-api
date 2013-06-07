from django.conf.urls import patterns, include, url
from atados_apiv1.views import *

urlpatterns = patterns(
    '',

    url(r'^project$', ProjectApi.as_view(), name='project'),
    url(r'^nonprofit$', NonprofitApi.as_view(), name='nonprofit'),
    url(r'^volunteer$', VolunteerApi.as_view(), name='volunteer'),
)
