from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, RedirectView
from django.views.generic.edit import UpdateView, FormMixin
from django.shortcuts import get_object_or_404
from django.utils.decorators import classonlymethod
from atados_core.forms import AddressForm
from atados_volunteer.models import Volunteer
from atados_volunteer.forms import (VolunteerPictureForm,
                                    VolunteerFirstStepForm,
                                    VolunteerSecondStepForm)


class UserReferenceMixin(object):
    only_owner = True
    user = None

    def get_context_data(self, **kwargs):
        context = super(UserReferenceMixin, self).get_context_data(**kwargs)
        context.update({'user_reference': self.get_user_reference()})
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.only_owner and request.user.username != kwargs.get('username'):
            raise Http404
        return super(UserReferenceMixin, self).dispatch(request,
                                                        *args, **kwargs)
 
    def get_user_reference(self):
        if self.user is None:
            self.user = get_object_or_404(User,
                                          username=self.kwargs.get('username'))
        return self.user

class VolunteerMixin(UserReferenceMixin):
    volunteer = None
    only_owner = True

    def get_context_data(self, **kwargs):
        context = super(VolunteerMixin, self).get_context_data(**kwargs)
        context.update({'volunteer': self.get_volunteer()})
        return context

    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.volunteer = get_object_or_404(Volunteer,
                                           user=self.get_user_reference())
        if self.only_owner and self.volunteer.user != request.user:
            raise PermissionDenied
        return super(VolunteerMixin, self).dispatch(request,
                                                    *args, **kwargs)

    def get_volunteer(self):
        return self.volunteer

class VolunteerBaseView(VolunteerMixin, TemplateView):
    pass

class VolunteerHomeView(TemplateView):
    template_name = 'atados_volunteer/home.html'

class VolunteerDetailsView(VolunteerBaseView):
    only_owner = False
    template_name = 'atados_volunteer/details.html'

class VolunteerPictureUpdateView(VolunteerMixin, UpdateView):
    model = Volunteer
    form_class=VolunteerPictureForm
    template_name='atados_volunteer/picture.html'
    get_object = VolunteerMixin.get_volunteer

class VolunteerFirstStepView(TemplateView, VolunteerMixin, FormMixin):
    template_name='atados_volunteer/first-step.html'
    
    def get_forms(self):
        return {
            'volunteer_form': VolunteerFirstStepForm(**self.get_volunteer_form_kwargs()),
            'address_form': AddressForm(**self.get_address_form_kwargs())
        }

    def get_address_form_kwargs(self):
        kwargs = super(VolunteerFirstStepView, self).get_form_kwargs()
        if self.object.address:
            kwargs.update({'instance': self.object.address})
        return kwargs

    def get_volunteer_form_kwargs(self):
        kwargs = super(VolunteerFirstStepView, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_volunteer()
        return self.render_to_response(self.get_context_data(**self.get_forms()))

    def post(self, request, *args, **kwargs):
        self.object = self.get_volunteer()
        forms = self.get_forms()
        if all([form.is_valid() for key, form in forms.iteritems()]):
            return self.form_valid(**forms)
        else:
            return self.form_invalid(**forms)

    def get_initial(self):
        volunteer = self.object

        initial = {
            'causes': set([cause.id for cause in volunteer.causes.all()]),
            'skills': set([skill.id for skill in volunteer.skills.all()]),
            'phone': volunteer.phone,
        };

        if (volunteer.address):
            initial.update({
                'zipcode': volunteer.address.zipcode,
                'addressline': volunteer.address.addressline,
                'addressnumber': volunteer.address.addressnumber,
                'neighborhood': volunteer.address.neighborhood,
                'state': volunteer.address.state,
                'city': volunteer.address.city,
                'suburb': volunteer.address.suburb,
            })

        return initial

    def get_success_url(self):
        return reverse('volunteer:second-step', args=(self.object.user.username,))

    def form_valid(self, volunteer_form, address_form):
        volunteer = volunteer_form.save(commit=False)
        volunteer.address = address_form.save()
        volunteer.save()
        volunteer_form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, volunteer_form, address_form):
        return self.render_to_response(self.get_context_data(
                volunteer_form=volunteer_form,
                address_form=address_form))

class VolunteerSecondStepView(VolunteerMixin, UpdateView):
    model = Volunteer
    form_class=VolunteerSecondStepForm
    template_name='atados_volunteer/second-step.html'
    get_object = VolunteerMixin.get_volunteer

    def get_success_url(self):
        return reverse('atados:home',)

class SocialNewUserView(RedirectView):

    def get_redirect_url(self):
        return reverse('volunteer:first-step', args=(self.request.user.username,))
