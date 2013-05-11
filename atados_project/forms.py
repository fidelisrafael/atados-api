# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from atados_core.forms import AddressForm
from atados_project.models import (Project,
                                   Donation,
                                   Work,
                                   Role)


class RoleForm(forms.ModelForm):

    class Meta:
        model = Role

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*arg, **kwargs)
        
        self.fields['prerequisites'].widget.attrs.update({'rows' : 5})
        
class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ('nonprofit', 'slug', 'published', 'deleted', 'deleted_date')

    def __init__(self, nonprofit, user, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.nonprofit = nonprofit

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : 'input-block-level'})


        self.fields['email'].widget.attrs.update({
            'placeholder' : _('example@example.com')})

        self.fields['details'].widget.attrs.update({
            'placeholder' : _('Add more info about this project')})

        self.fields['causes'].empty_label = ""
        self.fields['causes'].label = _("Select one or more causes")

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

class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation

class WorkForm(forms.ModelForm):

    class Meta:
        model = Work

    def __init__(self, *args, **kwargs):
        super(WorkForm, self).__init__(*args, **kwargs)
        self.fields['skills'].empty_label = ""
        self.fields['skills'].label = _("Select one or more skills")
        
class ProjectPictureForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('image',)
