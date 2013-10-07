from django.conf.urls import patterns, include, url
from atados_legacy.views import (LegacyBlogView,
                                 LegacyProjectView,
                                 LegacyNonprofitView)

urlpatterns = patterns('',

    # Legacy redirects
    url(r'^blog/(?P<path>.*)$', LegacyBlogView.as_view()),
    url(r'^site/ato/(?P<pk>[0-9]+)$', LegacyProjectView.as_view()),
    url(r'^site/instituicoes/(?P<pk>[0-9]+)/profile$', LegacyNonprofitView.as_view()),
)

