import os
from django import http
from django.utils import simplejson as json
from django.http import Http404
from django.views.generic import View
from django.views.generic.simple import direct_to_template
from django.contrib.auth.models import User
from atados.core.models import City, Suburb
from atados.volunteer.views import VolunteerDetailsView, VolunteerHomeView
from atados.volunteer.forms import RegistrationForm
from atados.nonprofit.views import NonprofitDetailsView, NonprofitHomeView
from atados.nonprofit.models import Nonprofit


template_name = 'atados/core/home.html'

def home(request, *args, **kwargs):
    if request.user.is_authenticated():
        try:
            Nonprofit.objects.get(user=request.user)
            return NonprofitHomeView.as_view()(request, *args, **kwargs)
        except Nonprofit.DoesNotExist:
            return VolunteerHomeView.as_view()(request, *args, **kwargs)

    return direct_to_template(request, 'atados/core/home.html',
                              {'form': RegistrationForm(),
                               'environ': os.environ})

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
