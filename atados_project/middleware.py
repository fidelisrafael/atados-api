from django.views.generic import TemplateView
from atados_project.views import (ProjectAwaitingModeration,
                                  AwaitingModerationView)


class ProjectAwaitingModerationMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.view_kwargs=view_kwargs

    def process_exception(self, request, exception):
        if isinstance(exception, ProjectAwaitingModeration):
            return AwaitingModerationView.as_view()(request, **self.view_kwargs)
