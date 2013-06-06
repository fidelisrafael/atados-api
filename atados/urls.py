from django.conf.urls import patterns, include, url
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.views.generic import TemplateView
from atados_core.views import slug

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url('', include('atados_core.urls', namespace='atados')),
    url('', include('atados_nonprofit.urls', namespace='nonprofit')),
    url('', include('atados_volunteer.urls', namespace='volunteer')),
    url('', include('atados_project.urls', namespace='project')),
    url(_(r'^(?P<slug>[-\w]+)$'), slug, name='slug'),
)

handler403 = TemplateView.as_view(template_name='403.html')
handler404 = TemplateView.as_view(template_name='404.html')
handler500 = TemplateView.as_view(template_name='500.html')

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
     'document_root': settings.MEDIA_ROOT}))
