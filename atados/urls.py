from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, url, include

admin.autodiscover()

urlpatterns = patterns('backend.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^', include('atados_core.urls'))
)
