# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from bootstrap_toolkit.widgets import BootstrapTextInput
from atados_core.models import State, City, Suburb
from atados_core.forms import LocationFormMixin
from atados_project.models import (Project,
                                   Donation,
                                   Work)


class ProjectCreateForm(LocationFormMixin, forms.ModelForm):

    def __init__(self, nonprofit, user, *args, **kwargs):
        super(ProjectCreateForm, self).__init__(*args, **kwargs)

        self.nonprofit = nonprofit

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : 'input-block-level'})

        self.fields['prerequisites'].widget.attrs.update({'rows' : 5})

        self.fields['email'].widget.attrs.update({
            'placeholder' : _('example@example.com')})

        self.fields['details'].widget.attrs.update({
            'placeholder' : _('Add more info about this project')})

        self.fields['causes'].empty_label = ""
        self.fields['causes'].label = _("Select one or more causes")

        self.prepare_location_fields()

    def save(self, commit=True):
        instance = super(ProjectCreateForm, self).save(commit)

        # save instance again to trigger RealTimeSearchIndex with m2m updated
        if commit:
            instance.save()

        return instance

    def clean_name(self):
        name = self.cleaned_data.get('name')
        slug = slugify(name)
        if slug and self.instance.slug != slug and Project.objects.filter(
                slug=slug, nonprofit=self.nonprofit, deleted=False).count():
            raise forms.ValidationError(_('This name (or a very similar) is already is use.'))
        return name

'''class ProjectDonationCreateForm(ProjectCreateForm):

    class Meta:
        model = ProjectDonation
        exclude = ('nonprofit', 'slug', 'published', 'deleted', 'deleted_date')

class ProjectWorkCreateForm(ProjectCreateForm):

    def __init__(self, *args, **kwargs):
        super(ProjectWorkCreateForm, self).__init__(*args, **kwargs)
        self.fields['skills'].empty_label = ""
        self.fields['skills'].label = _("Select one or more skills")
        
    class Meta:
        model = ProjectWork
        exclude = ('nonprofit', 'slug', 'published', 'deleted', 'deleted_date')'''

class ProjectPictureForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('image',)
