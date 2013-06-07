from django.conf.urls import patterns, include, url
from atados_apiv1.views import *

urlpatterns = patterns(
    '',

    url(r'^project$', ProjectApi.as_view(), name='project'),
    url(r'^nonprofit$', ProjectApi.as_view(), name='nonprofit'),
    url(r'^volunteer$', ProjectApi.as_view(), name='volunteer'),
)
