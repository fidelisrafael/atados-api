from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, RedirectView
from django.utils.translation import ugettext_lazy as _
from atados_core.forms import AuthenticationForm
from atados_core.views import HomeView, CityView, SuburbView, SearchView


urlpatterns = patterns(
    '',

    url(r'^$', HomeView.as_view(), name='home'),

    url(_(r'^sign-in$'), 'django.contrib.auth.views.login',
        {'authentication_form': AuthenticationForm,
         'template_name': 'atados_core/sign_in.html'}, name='sign-in'),

    url(r'^sign-in$', RedirectView.as_view(url=_('/sign-in'),
        query_string=True), name='global-sign-in'),

    url(_(r'^sign-out$'), 'django.contrib.auth.views.logout',
        {'next_page': _('/sign-in')}, name='sign-out'),

    url(_(r'^search$'), SearchView.as_view(), name='search'),

    url(_(r'^more-cities-soon$'), TemplateView.as_view(
        template_name='atados_core/more_cities_soon.html'), name='more-cities-soon'),

    url(_(r'^terms$'), TemplateView.as_view(
        template_name='atados_core/terms.html'), name='terms'),

    url(_(r'^privacy$'), TemplateView.as_view(
        template_name='atados_core/privacy.html'), name='privacy'),

    url(_(r'^security$'), TemplateView.as_view(
        template_name='atados_core/security.html'), name='security'),

    url(_(r'^about$'), TemplateView.as_view(
        template_name='atados_core/about.html'), name='about'),

    url(r'^city/(?P<state>[0-9]+)$', CityView.as_view()),
    url(r'^suburb/(?P<city>[0-9]+)$', SuburbView.as_view()),
)
