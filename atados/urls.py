from django.conf.urls import patterns, include, url
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from atados_core.views import slug

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('allauth.urls')),
    url('', include('atados_core.urls', namespace='atados')),
    url('', include('atados_nonprofit.urls', namespace='nonprofit')),
    url('', include('atados_volunteer.urls', namespace='volunteer')),
    url('', include('atados_legacy.urls', namespace='legacy')),
    url('', include('atados_project.urls', namespace='project')),
    url(r'^api/v1/', include('atados_apiv1.urls', namespace='apiv1')),
    url(_(r'^(?P<slug>[-\w]+)$'), slug, name='slug'),
)

handler500 = "atados_core.views.server_error"

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
     'document_root': settings.MEDIA_ROOT}))
