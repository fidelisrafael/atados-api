from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from atados.core.views import slug

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url('', include('atados.core.urls', namespace='atados')),
    url('', include('atados.nonprofit.urls', namespace='nonprofit')),
    url('', include('atados.volunteer.urls', namespace='volunteer')),
    url('', include('atados.project.urls', namespace='project')),
    url(_(r'^(?P<slug>[-\w]+)$'), slug, name='slug'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
     'document_root': settings.MEDIA_ROOT}))
