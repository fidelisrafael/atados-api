from django.views.generic import TemplateView
from atados_nonprofit.views import (NonprofitAwaitingModeration,
                                    AwaitingModerationView)
from atados_core.views import slug


class NonprofitAwaitingModerationMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.view_kwargs=view_kwargs

    def process_exception(self, request, exception):
        if isinstance(exception, NonprofitAwaitingModeration):
            if not 'nonprofit' in self.view_kwargs and 'slug' in self.view_kwargs:
                self.view_kwargs.update({
                    'nonprofit': self.view_kwargs['slug']
                })

            return AwaitingModerationView.as_view()(request, **self.view_kwargs)
