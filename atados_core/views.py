import os
from django import http
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseServerError
from django.template import RequestContext, TemplateDoesNotExist, loader
from django.utils import simplejson as json
from django.views.decorators.cache import cache_control, never_cache, cache_page
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import View, TemplateView
from django.views.generic.base import ContextMixin
from atados_core.models import City, Suburb, Cause, Skill
from atados_core.forms import SearchForm, AddressForm
from atados_volunteer.views import VolunteerDetailsView, VolunteerHomeView
from atados_volunteer.forms import RegistrationForm
from atados_nonprofit.models import Nonprofit
from atados_project.models import Project
from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet


@requires_csrf_token
def server_error(request, template_name='500.html'):
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseServerError('<h1>Server Error (500)</h1>')
    return HttpResponseServerError(template.render(RequestContext(request, {'request_path': request.path})))

def slug(request, *args, **kwargs):
    try:
        User.objects.get(username=kwargs['slug'])
        kwargs.update({
            'username': kwargs.pop('slug')
        })
        return VolunteerDetailsView.as_view()(request, *args, **kwargs)
    except User.DoesNotExist:
        try:
            Nonprofit.objects.get(slug=kwargs['slug'])
            kwargs.update({
                'nonprofit': kwargs.pop('slug')
            })
            from atados_nonprofit.views import NonprofitDetailsView
            return NonprofitDetailsView.as_view()(request, *args, **kwargs)
        except Nonprofit.DoesNotExist:
            raise Http404

class JSONResponseMixin(object):

    def render_to_response(self, context):
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        return http.HttpResponse(content, content_type='application/json', **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context)

class CityView(JSONResponseMixin, View):

    @cache_control(max_age=3600)
    def dispatch(self, *args, **kwargs):
        return super(CityView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = [{
            'id': city.pk,
            'name': city.name,
        } for city in City.objects.filter(state=kwargs['state'])]
        context.insert(0, {'id': '', 'name': ''})
        return self.render_to_response(context)

class SuburbView(JSONResponseMixin, View):

    @cache_control(max_age=3600)
    def dispatch(self, *args, **kwargs):
        return super(SuburbView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = [{
            'id': suburb.pk,
            'name': suburb.name,
        } for suburb in Suburb.objects.filter(city=kwargs['city'])]
        context.insert(0, {'id': '', 'name': ''})
        return self.render_to_response(context)

class CauseMixin(object):
    cause_list = None

    def __init__(self, *args, **kwargs):
        super(CauseMixin, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CauseMixin, self).get_context_data(**kwargs)
        context.update({'cause_list': self.cause_list})
        return context

class SearchView(FacetedSearchView, View):

    @never_cache
    def dispatch(self, *args, **kwargs):
        return super(SearchView, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        return super(SearchView, self).__call__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        kwargs['form_class'] = SearchForm
        kwargs['searchqueryset'] = SearchQuerySet().facet('causes').filter(published=True)
        super(FacetedSearchView, self).__init__(*args, **kwargs)

    def get_cause_list(self, context):
        cause_list = []
        for cause in Cause.objects.all():
            if 'fields' in context['facets']:
                total = dict(context['facets']['fields']['causes']).get(unicode(cause.id), 0)
            else:
                total = 0
            cause_list.append({
                'id': cause.id,
                'label': cause.name,
                'total': total,
            })
        return cause_list

    def get_skill_list(self, context):
        skill_list = []
        for skill in Skill.objects.all():
            if 'fields' in context['facets']:
                total = dict(context['facets']['fields']['skills']).get(unicode(skill.id), 0)
            else:
                total = 0
            skill_list.append({
                'id': skill.id,
                'label': skill.name,
                'total': total,
            })
        return skill_list

    def extra_context(self):
        context = super(SearchView, self).extra_context()
        context.update({
            'cause_list': self.get_cause_list(context),
            #'skill_list': self.get_skill_list(context),
        })
        return context

class HomeView(SearchView, View):
    template='atados_core/home.html'

    def build_form(self, form_kwargs=None):
        data = {u'types': [u'project']}
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(data, **kwargs)

    def extra_context(self):
        context = super(HomeView, self).extra_context()
        recommended = SearchQuerySet().models(Project).filter(has_image=True).filter(published=True).order_by('-id')[:3]
        context.update({
            'recommended': recommended,
            'address_form': AddressForm(),
        })
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                Nonprofit.objects.get(user=request.user)
                from atados_nonprofit.views import NonprofitHomeView
                return NonprofitHomeView.as_view()(request, *args, **kwargs)
            except Nonprofit.DoesNotExist:
                return VolunteerHomeView.as_view()(request, *args, **kwargs)

        return self.__call__(request, *args, **kwargs)
