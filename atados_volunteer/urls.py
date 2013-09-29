from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, RedirectView
from django.utils.translation import ugettext_lazy as _
from atados_volunteer.views import (VolunteerPictureUpdateView,
                                    VolunteerFirstStepView,
                                    VolunteerSecondStepView,
                                    SocialNewUserView)
urlpatterns = patterns(
    '',

    url(_(r'^volunteer/signup-complete$'),
        TemplateView.as_view(template_name='atados_volunteer/signup-complete.html'),
        name='signup-complete'),

    url(_(r'^volunteer/profile$'),
        TemplateView.as_view(template_name='atados_volunteer/signup-complete.html'),
        name='profile'),

    url(_(r'^(?P<username>[-\w]+)/edit$'),
        VolunteerPictureUpdateView.as_view(),
        name='edit'),

    url(_(r'^(?P<username>[-\w]+)/edit-volunteer-picture$'),
        VolunteerPictureUpdateView.as_view(),
        name='edit-volunteer-picture'),

    url(_(r'^(?P<username>[-\w]+)/volunteer/first-step$'),
        VolunteerFirstStepView.as_view(),
        name='first-step'),

    url(_(r'^(?P<username>[-\w]+)/volunteer/second-step$'),
            VolunteerSecondStepView.as_view(),
        name='second-step'),
)

