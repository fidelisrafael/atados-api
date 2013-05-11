from django.http import Http404
from django.views.generic import TemplateView, View
from django.views.generic.edit import (CreateView, ModelFormMixin, UpdateView,
                                       DeleteView, FormMixin)
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _, ugettext as __
from atados_core.forms import SearchForm
from atados_core.views import JSONResponseMixin, SearchView
from atados_volunteer.models import Volunteer
from atados_project.models import (Project, Donation, Work, Apply,
                                   Availability)
from atados_nonprofit.models import Nonprofit
from atados_nonprofit.views import NonprofitMixin
from atados_project.forms import (DonationForm,
                                  WorkForm,
                                  ProjectForm,
                                  RoleForm,
                                  ProjectPictureForm)


class AvailabilityMixin(object):
    availability_list = None

    def __init__(self, *args, **kwargs):
        super(AvailabilityMixin, self).__init__(*args, **kwargs)
        self.availability_list = Availability.objects.all()


    def get_context_data(self, **kwargs):
        context = super(AvailabilityMixin, self).get_context_data(**kwargs)
        context.update({'availability_list': self.availability_list})
        return context

class ProjectMixin(NonprofitMixin):
    project = None

    def get_context_data(self, **kwargs):
        context = super(ProjectMixin, self).get_context_data(**kwargs)
        context.update({'project': self.get_project()})
        return context

    def get_project(self):
        if self.project is None:
            try:
                self.project = ProjectWork.objects.get(
                    nonprofit=self.get_nonprofit(),
                    slug=self.kwargs.get('project'),
                    deleted=False)
            except ProjectWork.DoesNotExist:
                try:
                    self.project = ProjectJob.objects.get(
                        nonprofit=self.get_nonprofit(),
                        slug=self.kwargs.get('project'),
                        deleted=False)
                except ProjectJob.DoesNotExist:
                    try:
                        self.project = ProjectDonation.objects.get(
                            nonprofit=self.get_nonprofit(),
                            slug=self.kwargs.get('project'),
                            deleted=False)
                    except ProjectDonation.DoesNotExist:
                        raise Http404

        return self.project

class ProjectView(TemplateView, NonprofitMixin, FormMixin):

    def get(self, request, *args, **kwargs):
        project_form = self.get_form(ProjectForm)
        work_form = self.get_form(WorkForm)
        role_form = self.get_form(RoleForm)
        return super(ProjectView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        project_form = self.get_form(ProjectForm)
        work_form = self.get_form(WorkForm)
        role_form = self.get_form(RoleForm)
        if (project_form.is_valid() and
            work_form.is_valid() and
            role_form.is_valid()):
            return self.form_valid(project_form, work_form, role_form)
        else:
            return self.form_invalid(project_form, work_form, role_form)

    def get_initial(self):
        nonprofit = self.get_nonprofit()

        return {
            'causes': set([cause.id for cause in nonprofit.causes.all()]),
            'zipcode': nonprofit.zipcode,
            'addressline': nonprofit.addressline,
            'addressnumber': nonprofit.addressnumber,
            'neighborhood': nonprofit.neighborhood,
            'responsible': self.request.user.first_name,
            'email': self.request.user.email,
            'phone': nonprofit.phone,
            'state': nonprofit.state,
            'city': nonprofit.city,
            'suburb': nonprofit.suburb,
        };

    def get_form(self, form_class):
        if form_class == ProjectForm:
            return form_class(**self.get_project_form_kwargs())
        return form_class(**self.get_form_kwargs())

    def get_project_form_kwargs(self):
        kwargs = super(ProjectView, self).get_form_kwargs()
        kwargs.update({
            'nonprofit': self.get_nonprofit(),
            'user': self.request.user,
        })
        return kwargs

    def form_valid(self, project_form, work_form, role_form):
        model = form.save(commit=False)
        if self.request.user.is_authenticated():
            model.nonprofit = Nonprofit.objects.get(user=self.request.user)
            model.slug = slugify(model.name)
        else:
            forms.ValidationError("Authentication required")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, project_form, work_form, role_form):
        return self.render_to_response(self.get_context_data(
            project_form=project_form,
            work_form=work_form,
            role_form=role_form))


class ProjectDonationCreateView(TemplateView):
    template_name='atados_project/new-donation.html'

class ProjectWorkCreateView(TemplateView):
    template_name='atados_project/new-work.html'

class ProjectJobCreateView(ProjectView):
    template_name='atados_project/new-job.html'

class ProjectDetailsView(ProjectMixin, DetailView):
    only_owner=False

    def get_volunteer(self):
        if self.request.user.is_authenticated():
            try:
                return Volunteer.objects.get(user=self.request.user)
            except Volunteer.DoesNotExist:
                pass
        return None

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailsView, self).get_context_data(**kwargs)
        
        volunteer = self.get_volunteer()

        if volunteer is not None:
            try:
                context.update({'apply': Apply.objects.get(
                    project=self.get_project(),
                    volunteer=volunteer)})
            except Apply.DoesNotExist:
                pass

        return context

    def get_template_names(self):
        if isinstance(self.object, ProjectDonation):
            return 'atados_project/details-donation.html'
        if isinstance(self.object, ProjectJob):
            return 'atados_project/details-job.html'
        if isinstance(self.object, ProjectWork):
            return 'atados_project/details-work.html'
        raise Http404

    get_object = ProjectMixin.get_project

class ProjectCollaboratorsView(ProjectMixin, TemplateView):
    template_name = 'atados_project/collaborators.html'

class ProjectDeleteView(ProjectMixin, TemplateView):
    template_name = 'atados_project/delete.html'

class ProjectApplyView(ProjectMixin, JSONResponseMixin, View):
    only_owner = False

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            context = {'success': False,
                       'errors': __('Login required')}
            return self.render_to_response(context)

        Apply(project=self.get_project(), volunteer=Volunteer.objects.get(user=request.user)).save()

        context = {'success': True,
                   'msg': ''}
        return self.render_to_response(context)

    get = post

class ProjectPictureUpdateView(ProjectMixin, UpdateView):
    model = Project
    form_class=ProjectPictureForm
    template_name='atados_project/picture.html'
    get_object = ProjectMixin.get_project

class ProjectDeleteView(ProjectMixin, DeleteView):
    get_object = ProjectMixin.get_project
    template_name='atados_project/delete.html'

    def get_success_url(self):
        messages.info(self.request, _('Project was successfully deleted.'))
        return reverse('atados:home')

class ProjectSearchView(SearchView):
    template = 'atados_project/index.html'
