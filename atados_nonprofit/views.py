from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, FormMixin
from django.shortcuts import get_object_or_404
from django.utils.decorators import classonlymethod
from atados_core.forms import AddressForm
from atados_nonprofit.models import Nonprofit
from atados_nonprofit.forms import (NonprofitPictureForm,
                                    NonprofitCoverForm,
                                    NonprofitFirstStepForm,
                                    NonprofitSecondStepForm,
                                    NonprofitDetailsForm)


class NonprofitMixin(object):
    nonprofit = None
    only_owner = True

    def get_context_data(self, **kwargs):
        kwargs.update({
            'nonprofit': self.get_nonprofit(),
        })
        return super(NonprofitMixin, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.nonprofit = get_object_or_404(Nonprofit,
                                           slug=kwargs.get('nonprofit'))

        if not self.nonprofit.published and not self.only_owner:
            raise Http404

        if self.only_owner and self.nonprofit.user != request.user:
            raise PermissionDenied
        return super(NonprofitMixin, self).dispatch(request,
                                                    *args, **kwargs)

    def get_nonprofit(self):
        return self.nonprofit

class NonprofitBaseView(NonprofitMixin, TemplateView):
    pass

class NonprofitHomeView(TemplateView):
    template_name = 'atados_nonprofit/home.html'

class NonprofitDetailsView(NonprofitBaseView):
    only_owner = False
    template_name = 'atados_nonprofit/details.html'

class NonprofitPictureUpdateView(NonprofitMixin, UpdateView):
    model = Nonprofit
    form_class=NonprofitPictureForm
    template_name='atados_nonprofit/picture.html'
    get_object = NonprofitMixin.get_nonprofit

class NonprofitCoverUpdateView(NonprofitMixin, UpdateView):
    model = Nonprofit
    form_class=NonprofitCoverForm
    template_name='atados_nonprofit/cover.html'
    get_object = NonprofitMixin.get_nonprofit

class NonprofitDetailsUpdateView(NonprofitMixin, UpdateView):
    model = Nonprofit
    form_class=NonprofitDetailsForm
    template_name='atados_nonprofit/edit.html'
    get_object = NonprofitMixin.get_nonprofit

class NonprofitFirstStepView(TemplateView, NonprofitMixin, FormMixin):
    template_name='atados_nonprofit/first-step.html'

    def get_forms(self):
        return {
            'nonprofit_form': NonprofitFirstStepForm(**self.get_nonprofit_form_kwargs()),
            'address_form': AddressForm(**self.get_address_form_kwargs())
        }

    def get_address_form_kwargs(self):
        kwargs = super(NonprofitFirstStepView, self).get_form_kwargs()
        if self.object.address:
            kwargs.update({'instance': self.object.address})
        return kwargs

    def get_nonprofit_form_kwargs(self):
        kwargs = super(NonprofitFirstStepView, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_nonprofit()
        return self.render_to_response(self.get_context_data(**self.get_forms()))

    def post(self, request, *args, **kwargs):
        self.object = self.get_nonprofit()
        forms = self.get_forms()
        if all([form.is_valid() for key, form in forms.iteritems()]):
            return self.form_valid(**forms)
        else:
            return self.form_invalid(**forms)

    def get_initial(self):
        nonprofit = self.object

        initial = {
            'causes': set([cause.id for cause in nonprofit.causes.all()]),
            'phone': nonprofit.phone,
        };

        if (nonprofit.address):
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
    
    def get_success_url(self):
        return reverse('nonprofit:second-step', args=(self.nonprofit.slug,))

    def form_valid(self, nonprofit_form, address_form):
        nonprofit = nonprofit_form.save(commit=False)
        nonprofit.address = address_form.save()
        nonprofit.save()
        nonprofit_form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, nonprofit_form, address_form):
        return self.render_to_response(self.get_context_data(
                nonprofit_form=nonprofit_form,
                address_form=address_form))

class NonprofitSecondStepView(NonprofitMixin, UpdateView):
    model = Nonprofit
    form_class=NonprofitSecondStepForm
    template_name='atados_nonprofit/second-step.html'
    get_object = NonprofitMixin.get_nonprofit

    def get_success_url(self):
        return reverse('atados:home',)
