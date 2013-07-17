# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from bootstrap_toolkit.widgets import BootstrapTextInput
from registration.forms import RegistrationForm as DefaultRegistrationForm
from atados_nonprofit.models import Nonprofit
from atados_volunteer.models import Volunteer
from atados_core.forms import AddressForm


class RegistrationForm(DefaultRegistrationForm):

    first_name = forms.CharField(max_length=30,
                           widget=forms.TextInput(
                               attrs={'class': 'required',
                                      'placeholder': _("Your first name")}),
                           label=_("Name"))

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs=dict({'class': 'required',
                        'placeholder': _("example@example.com")},
                       maxlength=75)),
        label=_("Your e-mail"))

    username = forms.RegexField(regex=r'^[\w-]+$',
                                max_length=30,
                                widget=BootstrapTextInput(
                                    prepend='http://www.atados.com.br/',
                                    attrs={'class': 'required'}),
                                label=_("Username"),
                                error_messages={'invalid':
                                                _("This value may contain "
                                                  "only letters, numbers a"
                                                  "nd \"-\" character.")
                                                })

    password1 = forms.CharField(widget=forms.PasswordInput(
    attrs={'class': 'required'}, render_value=False),
    label=_("Create a password"))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'required'}, render_value=False),
        label=_("Confirm your password"))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : 'input-block-level'})

        self.fields.keyOrder = ['first_name',
                                'email',
                                'username',
                                'password1',
                                'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and (
                User.objects.filter(username=username).count() or
                Nonprofit.objects.filter(slug=username).count()):
            raise forms.ValidationError(_('This username is already is use.'))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(
                username=username).count():
            raise forms.ValidationError(_('This e-mail is already is use.'))
        return email

class VolunteerPictureForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ('image',)

class VolunteerFirstStepForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(VolunteerFirstStepForm, self).__init__(*args, **kwargs)

        self.fields['causes'].empty_label = ""
        self.fields['causes'].label = _("Select one or more causes")

        self.fields['skills'].empty_label = ""
        self.fields['skills'].label = _("Select one or more skills")

    class Meta:
        model = Volunteer
        fields = ('causes', 'skills', 'phone',)
        
class VolunteerSecondStepForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ('image',)
