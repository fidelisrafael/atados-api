from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, View
from django.views.generic.edit import (CreateView, ModelFormMixin, UpdateView,
                                       DeleteView, FormMixin)
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _, ugettext as __
from atados.settings import STATIC_URL
from atados_core.forms import AddressForm, SearchForm
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
from haystack.query import SearchQuerySet
from sorl.thumbnail import get_thumbnail


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
            self.project = get_object_or_404(Project, 
                                             nonprofit=self.get_nonprofit(),
                                             slug=self.kwargs.get('project'),
                                             deleted=False)
        return self.project

class ProjectView(TemplateView, NonprofitMixin, FormMixin):
    project=None

    def get_forms(self):
        return {
            'project_form': self.get_project_form(),
        }

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**self.get_forms()))

    def post(self, request, *args, **kwargs):
        forms = self.get_forms(request)
        if all([form.is_valid() for key, form in forms.iteritems()]):
            return self.form_valid(**forms)
        else:
            return self.form_invalid(**forms)

    def get_initial(self):
        nonprofit = self.get_nonprofit()

        initial = {
            'causes': set([cause.id for cause in nonprofit.causes.all()]),
            'responsible': self.request.user.first_name,
            'email': self.request.user.email,
            'phone': nonprofit.phone,
        };

        if nonprofit.address:
            initial.update({
                'zipcode': nonprofit.address.zipcode,
                'addressline': nonprofit.address.addressline,
                'addressnumber': nonprofit.address.addressnumber,
                'neighborhood': nonprofit.address.neighborhood,
                'state': nonprofit.address.state,
                'city': nonprofit.address.city,
                'suburb': nonprofit.address.suburb,
            })


        return initial

    def get_success_url(self, project):
        return reverse('project:details',
                       args=[self.get_nonprofit().slug, project.slug])

    def get_project_form(self):
        return ProjectForm(**self.get_project_form_kwargs())

    def get_project_form_kwargs(self):
        kwargs = super(ProjectView, self).get_form_kwargs()
        kwargs.update({
            'nonprofit': self.get_nonprofit(),
            'user': self.request.user,
        })
        return kwargs

    def form_invalid(self, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**self.get_forms()))

    def save_project(self, project_form):
        project = project_form.save(commit=False)
        project.nonprofit = Nonprofit.objects.get(user=self.request.user)
        project.slug = slugify(project.name)
        return project_form.save()


class ProjectDonationCreateView(ProjectView):
    template_name='atados_project/new-donation.html'

    def get_forms(self, request=None):
        forms = super(ProjectDonationCreateView, self).get_forms()
        forms.update({
            'donation_form': self.get_form(DonationForm),
            'address_form': self.get_form(AddressForm),
        })
        return forms

    def form_valid(self, project_form, donation_form, address_form):
        if not self.request.user.is_authenticated():
            forms.ValidationError("Authentication required")

        project = self.save_project(project_form)

        address = address_form.save()

        donation = donation_form.save(commit=False)
        donation.project = project
        donation.delivery = address
        donation = donation.save()

        return HttpResponseRedirect(self.get_success_url(project))

class ProjectWorkCreateView(ProjectView):
    template_name='atados_project/new-work.html'

    def get_forms(self, request=None):
        RoleFormset = formset_factory(RoleForm)
        forms = super(ProjectWorkCreateView, self).get_forms()
        forms.update({
            'work_form': self.get_form(WorkForm),
            'address_form': self.get_form(AddressForm),
        })

        if (request):
            forms.update({
                'role_formset': RoleFormset(self.request.POST, self.request.FILES),
            })
        else:
            forms.update({'role_formset': RoleFormset(),})
        return forms

    def form_valid(self, project_form, work_form, role_formset, address_form):
        if not self.request.user.is_authenticated():
            forms.ValidationError("Authentication required")

        project = self.save_project(project_form)

        address = address_form.save()

        work = work_form.save(commit=False)
        work.project = project
        work.address = address
        work = work_form.save()

        for role_form in role_formset.forms:
            if role_form.has_changed():
                role = role_form.save(commit=False)
                role.work = work
                role = role_form.save()

        return HttpResponseRedirect(self.get_success_url(project))

class ProjectJobCreateView(ProjectWorkCreateView):
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
        return 'atados_project/details-donation.html'
        return 'atados_project/details-work.html'

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
