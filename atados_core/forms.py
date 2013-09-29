# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from haystack.forms import FacetedSearchForm, model_choices
from atados_nonprofit.models import Nonprofit
from atados_project.models import Project
from atados_volunteer.models import Volunteer
from atados_core.models import Address, State, City, Suburb, Cause, Skill, Availability


SEARCH_TYPES = (
        ('nonprofit', 'nonprofit'),
        ('project', 'project'),
        ('volunteer', 'volunteer'),)

class SearchForm(FacetedSearchForm):
    causes = forms.MultipleChoiceField(required=False,
                                       widget=forms.CheckboxSelectMultiple,
                                       choices=((cause.id, cause.name) for cause in Cause.objects.all()))

    skills = forms.MultipleChoiceField(required=False,
                                       widget=forms.CheckboxSelectMultiple,
                                       choices=((skill.id, skill.name) for skill in Skill.objects.all()))

    state = forms.MultipleChoiceField(required=False,
                                      widget=forms.CheckboxSelectMultiple,
                                      choices=((state.id, state.name) for state in State.objects.all()))

    city = forms.MultipleChoiceField(required=False,
                                     widget=forms.CheckboxSelectMultiple,
                                     choices=((city.id, city.name) for city in City.objects.all()))

    suburb = forms.MultipleChoiceField(required=False,
                                       widget=forms.CheckboxSelectMultiple,
                                       choices=((suburb.id, suburb.name) for suburb in Suburb.objects.all()))

    availabilities = forms.MultipleChoiceField(required=False,
                                               widget=forms.CheckboxSelectMultiple,
                                               choices=((availability.id, availability) for availability in Availability.objects.all()))

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['types'] = forms.MultipleChoiceField(choices=SEARCH_TYPES, required=False, label=_('Search in'), widget=forms.CheckboxSelectMultiple)

    def get_models(self):
        """Return an alphabetical list of model classes in the index."""
        search_models = []

        if self.is_valid():
            if 'nonprofit' in self.cleaned_data['types']:
                search_models.append(Nonprofit)
            if 'volunteer' in self.cleaned_data['types']:
                search_models.append(Volunteer)
            if 'project' in self.cleaned_data['types'] or not search_models:
                search_models.append(Project)

        return search_models

    def no_query_found(self):
        return self.searchqueryset.all()

    def search(self):
        sqs = super(SearchForm, self).search()

        if self.is_bound:
            if 'causes' in self.cleaned_data and self.cleaned_data['causes']:
                sqs = sqs.narrow(u'causes_exact:(%s)' % ' OR '.join([sqs.query.clean(cause) for cause in self.cleaned_data['causes']]))
            if 'skills' in self.cleaned_data and self.cleaned_data['skills']:
                sqs = sqs.narrow(u'skills_exact:(%s)' % ' OR '.join([sqs.query.clean(skill) for skill in self.cleaned_data['skills']]))

            if 'state' in self.cleaned_data and self.cleaned_data['state']:
                sqs = sqs.narrow(u'state_exact:(%s)' % ' OR '.join([sqs.query.clean(state) for state in self.cleaned_data['state']]))
            if 'city' in self.cleaned_data and self.cleaned_data['city']:
                sqs = sqs.narrow(u'city_exact:(%s)' % ' OR '.join([sqs.query.clean(city) for city in self.cleaned_data['city']]))
            if 'suburb' in self.cleaned_data and self.cleaned_data['suburb']:
                sqs = sqs.narrow(u'suburb_exact:(%s)' % ' OR '.join([sqs.query.clean(suburb) for suburb in self.cleaned_data['suburb']]))

            if 'availabilities' in self.cleaned_data and self.cleaned_data['availabilities']:
                sqs = sqs.narrow(u'availabilities_exact:(%s)' % ' OR '.join([sqs.query.clean(availability) for availability in self.cleaned_data['availabilities']]))

        return sqs.models(*self.get_models())

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address

    def __init__(self, *args, **kwargs):
        no_state = kwargs.pop('no_state', False)

        super(AddressForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : 'input-block-level'})

        self.fields['state'].empty_label = ""
        self.fields['city'].empty_label = ""
        self.fields['suburb'].empty_label = ""

        if no_state:
            self.fields['city'].queryset = City.objects.all()
        else:
            if self.is_bound:
                if 'state' in self.data and self.data['state']:
                    self.fields['city'].queryset = City.objects.filter(state=self.data['state'])
                else:
                    self.fields['city'].queryset = City.objects.none()
            else:
                self.fields['city'].queryset = City.objects.filter(state=self.initial.get('state'))

        if self.is_bound:
            if 'city' in self.data and self.data['city']:
                self.fields['suburb'].queryset = Suburb.objects.filter(city=self.data['city'])
            else:
                self.fields['suburb'].queryset = Suburb.objects.none()
        else:
            self.fields['suburb'].queryset = Suburb.objects.filter(city=self.initial.get('city'))
