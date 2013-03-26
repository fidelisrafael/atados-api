from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template, redirect_to
from django.utils.translation import ugettext_lazy as _
from atados.core.forms import AuthenticationForm
from atados.volunteer.views import (VolunteerPictureUpdateView,
                                    VolunteerFirstStepView,
                                    VolunteerSecondStepView)
from registration.views import register, activate

urlpatterns = patterns(
    '',

    url(_(r'^volunteer/sign-up$'), register,
        {'backend': 'atados.volunteer.backends.RegistrationBackend',
         'template_name': 'atados/volunteer/sign-up.html'},
        name='sign-up'),

    url(_(r'^volunteer/sign-up-confirmartion/(?P<activation_key>\w+)$'), activate,
        {'backend': 'atados.volunteer.backends.RegistrationBackend',
         'template_name': 'atados/volunteer/sign-up-activation.html'},
        name='sign-up-confirmation'),

    url(_(r'^volunteer/sign-up-complete$'), direct_to_template, {'template': 'atados/volunteer/sign-up-complete.html'},
        name='sign-up-complete'),

    url(_(r'^volunteer/profile$'), direct_to_template, {'template': 'atados/volunteer/sign-up-complete.html'},
        name='profile'),

    url(_(r'^(?P<username>[-\w]+)/edit-volunteer-picture$'), VolunteerPictureUpdateView.as_view(),
        name='edit-volunteer-picture'),

    url(_(r'^(?P<username>[-\w]+)/volunteer/first-step$'), VolunteerFirstStepView.as_view(),
        name='first-step'),

    url(_(r'^(?P<username>[-\w]+)/volunteer/second-step$'), VolunteerSecondStepView.as_view(),
        name='second-step'),

)

