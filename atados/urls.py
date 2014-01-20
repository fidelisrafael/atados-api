from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, url, include

admin.autodiscover()

urlpatterns = patterns('backend.views',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('atados_core.urls'))
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
