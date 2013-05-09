import os
from django import http
from django.utils import simplejson as json
from django.http import Http404
from django.views.generic import View, TemplateView
from django.contrib.auth.models import User
from atados_core.models import City, Suburb, Cause, Skill
from atados_core.forms import SearchForm
from atados_volunteer.views import VolunteerDetailsView, VolunteerHomeView
from atados_volunteer.forms import RegistrationForm
from atados_nonprofit.views import NonprofitDetailsView, NonprofitHomeView
from atados_nonprofit.models import Nonprofit
from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet


template_name = 'atados_core/home.html'

class HomeView(TemplateView):
    template_name='atados_core/home.html'

    def get_context_date(self):
        return {'form': RegistrationForm(),
                'environ': os.environ}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                Nonprofit.objects.get(user=request.user)
                return NonprofitHomeView.as_view()(request, *args, **kwargs)
            except Nonprofit.DoesNotExist:
                return VolunteerHomeView.as_view()(request, *args, **kwargs)

        return super(HomeView, self).get(request, *args, **kwargs)



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

    def get(self, request, *args, **kwargs):
        context = [{
            'id': city.pk,
            'name': city.name,
        } for city in City.objects.filter(state=kwargs['state'])]
        context.insert(0, {'id': '', 'name': ''})
        return self.render_to_response(context)

class SuburbView(JSONResponseMixin, View):

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

class SearchView(FacetedSearchView):

    def __init__(self, *args, **kwargs):
        kwargs['form_class'] = SearchForm
        kwargs['searchqueryset'] = SearchQuerySet().facet('causes').facet('skills')
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
            'skill_list': self.get_skill_list(context),
        })
        return context
