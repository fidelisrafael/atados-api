from django.http import Http404
from django.views.decorators.cache import cache_control, never_cache, cache_page
from django.views.generic import View
from atados_core.views import JSONResponseMixin, SearchView
from sorl.thumbnail import get_thumbnail
from atados.settings import STATIC_URL


def get_thumb(image, width, height):
    size = "%sx%s" % (width, height)

    try:
        url = get_thumbnail(image, size, crop='center').url
    except:
        url = STATIC_URL + 'img/thumb/' + size + '.gif'

    return {'url': url,
            'width': width,
            'height': height,}

class ProjectApi(SearchView, JSONResponseMixin, View):

    @never_cache
    def dispatch(self, *args, **kwargs):
        return super(ProjectApi, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.__call__(request)

    def create_response(self):
        try:
            (paginator, page) = self.build_page()

            context = [{
                'id': result.object.id,
                'image': get_thumb(result.object.image, 270, 180),
                'url': result.object.get_absolute_url(),
                'name': result.object.name,
                'details': result.object.get_description(),
                'volunteers': len(result.object.apply_set.all()),
                'nonprofit': {
                    'image': get_thumb(result.object.nonprofit.image, 34, 34),
                    'url': result.object.nonprofit.get_absolute_url(),
                    'name': result.object.nonprofit.name,
                }
            } for result in page.object_list]
        except Http404:
            context = []

        return self.render_to_response(context)


class NonprofitApi(SearchView, JSONResponseMixin, View):

    @never_cache
    def dispatch(self, *args, **kwargs):
        return super(NonprofitApi, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.__call__(request)

    def build_form(self, form_kwargs=None):
        data = {u'types': [u'nonprofit']}
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(data, **kwargs)

    def create_response(self):
        (paginator, page) = self.build_page()

        context = [{
            'id': result.object.id,
            'image': get_thumb(result.object.image, 270, 270),
            'url': result.object.get_absolute_url(),
            'name': result.object.name,
        } for result in page.object_list]
        return self.render_to_response(context)


class VolunteerApi(SearchView, JSONResponseMixin, View):

    @never_cache
    def dispatch(self, *args, **kwargs):
        return super(VolunteerApi, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.__call__(request)

    def build_form(self, form_kwargs=None):
        data = {u'types': [u'volunteer']}
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(data, **kwargs)

    def create_response(self):
        (paginator, page) = self.build_page()

        context = [{
            'id': result.object.id,
            'image': get_thumb(result.object.image, 270, 180),
            'url': result.object.get_absolute_url(),
            'name': result.object.user.first_name + ' ' +
                    result.object.user.last_name ,
        } for result in page.object_list]
        return self.render_to_response(context)
