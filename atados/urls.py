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
    url('', include('atados_core.urls', namespace='atados')),
    url('', include('atados_nonprofit.urls', namespace='nonprofit')),
    url('', include('atados_volunteer.urls', namespace='volunteer')),
    url('', include('atados_project.urls', namespace='project')),
    url('', include('atados_legacy.urls', namespace='legacy')),
    url(_(r'^(?P<slug>[-\w]+)$'), slug, name='slug'),
    url('', include('allauth.urls')),
    # url(r'api/', include('rest_framework.urls', namespace='rest_framework')),
)

handler500 = "atados_core.views.server_error"

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
     'document_root': settings.MEDIA_ROOT}))
