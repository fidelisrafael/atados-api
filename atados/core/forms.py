# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm as ContribAuthenticationForm)
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm as HaystackSearchForm, model_choices
from atados.nonprofit.models import Nonprofit
from atados.project.models import ProjectDonation, ProjectWork
from atados.volunteer.models import Volunteer
from atados.core.models import State, City, Suburb


SEARCH_TYPES = (
        ('Nonprofit', 'Nonprofit'),
        ('Project', 'Project'),
        ('Volunteer', 'Volunteer'),)

class SearchForm(HaystackSearchForm):
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['types'] = forms.MultipleChoiceField(choices=SEARCH_TYPES, required=False, label=_('Search in'), widget=forms.CheckboxSelectMultiple)

    def get_models(self):
        """Return an alphabetical list of model classes in the index."""
        search_models = []

        if self.is_valid():
            if 'Nonprofit' in self.cleaned_data['types']:
                search_models.append(Nonprofit)
            if 'Volunteer' in self.cleaned_data['types']:
                search_models.append(Volunteer)
            if 'Project' in self.cleaned_data['types'] or not search_models:
                search_models.append(ProjectDonation)
                search_models.append(ProjectWork)

        return search_models

    def search(self):
        sqs = super(SearchForm, self).search()
        return sqs.models(*self.get_models())

class AuthenticationForm(ContribAuthenticationForm):
    username = forms.CharField(label=_('E-mail'), max_length=30)
    rememberme = forms.BooleanField(label=_('Stay signed in'),
                                    initial=True, required=False)

class LocationFormMixin(object):

    def prepare_location_fields(self):
        self.fields['state'].empty_label = ""
        self.fields['city'].empty_label = ""
        self.fields['suburb'].empty_label = ""

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