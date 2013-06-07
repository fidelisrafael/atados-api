from django.views.generic import View
from atados_core.views import JSONResponseMixin, SearchView
from sorl.thumbnail import get_thumbnail


class ProjectApi(SearchView, JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        return self.__call__(request);

    def create_response(self):
        (paginator, page) = self.build_page()

        def get_image(image, size):
            try:
                return get_thumbnail(image, size, crop='center').url
            except:
                return STATIC_URL + 'img/thumb/300.gif';

        context = [{
            'id': result.object.id,
            'image': get_image(result.object.image, '270x270'),
            'url': result.object.get_absolute_url(),
            'name': result.object.name,
            'details': result.object.get_description(),
            'volunteers': 0,
            'nonprofit': {
                'image': get_image(result.object.nonprofit.image, '34x34'),
                'url': result.object.nonprofit.get_absolute_url(),
                'name': result.object.nonprofit.name,
            }
        } for result in page.object_list]
        return self.render_to_response(context)
