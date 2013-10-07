from django.views.generic import TemplateView, RedirectView
from django.shortcuts import get_object_or_404
from atados_core.models import Nonprofit, Project
from django.contrib.auth.models import User


class LegacyNonprofitView(RedirectView):
    permanent = True
    query_string = False
    def get_redirect_url(self, pk):
        user = get_object_or_404(User, pk=pk)
        return get_object_or_404(Nonprofit, user=user).get_absolute_url()

class LegacyProjectView(RedirectView):
    permanent = True
    query_string = False
    def get_redirect_url(self, pk):
        return get_object_or_404(Project, pk=pk).get_absolute_url()

class LegacyBlogView(RedirectView):
    permanent = True
    url = 'http://blog.atados.com.br/%(path)s'
    query_string = True
