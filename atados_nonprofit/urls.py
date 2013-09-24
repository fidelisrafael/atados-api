from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, RedirectView
from django.utils.translation import ugettext_lazy as _
from atados_core.forms import AuthenticationForm
from atados_nonprofit.views import (NonprofitPictureUpdateView,
                                    NonprofitCoverUpdateView,
                                    NonprofitFirstStepView,
                                    NonprofitSecondStepView,
                                    NonprofitDetailsUpdateView)

urlpatterns = patterns(
    '',

#url(_(r'^nonprofit/sign-up$'), register,
#       {'backend': 'atados_nonprofit.backends.RegistrationBackend',
#        'template_name': 'atados_nonprofit/sign-up.html'},
#      name='sign-up'),

#    url(_(r'^nonprofit/sign-up-confirmartion/(?P<activation_key>\w+)$'), activate,
#       {'backend': 'atados_nonprofit.backends.RegistrationBackend',
#        'template_name': 'atados_nonprofit/sign-up-activation.html'},
#       name='sign-up-confirmation'),

    url(_(r'^(?P<nonprofit>[-\w]+)/nonprofit/first-step$'), NonprofitFirstStepView.as_view(),
        name='first-step'),

    url(_(r'^(?P<nonprofit>[-\w]+)/nonprofit/second-step$'), NonprofitSecondStepView.as_view(),
        name='second-step'),

    url(_(r'^nonprofit/sign-up-complete$'), TemplateView.as_view(template_name='atados_nonprofit/sign-up-complete.html'),
        name='sign-up-complete'),

    url(_(r'^(?P<nonprofit>[-\w]+)/edit-nonprofit-picture$'), NonprofitPictureUpdateView.as_view(),
        name='edit-nonprofit-picture'),

    url(_(r'^(?P<nonprofit>[-\w]+)/edit-nonprofit-cover$'), NonprofitCoverUpdateView.as_view(),
        name='edit-nonprofit-cover'),

    url(_(r'^(?P<nonprofit>[-\w]+)/edit$'), NonprofitDetailsUpdateView.as_view(),
        name='edit'),
)
