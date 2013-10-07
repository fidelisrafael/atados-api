from django.contrib.sites.models import Site
from atados_core.models import Volunteer, Nonprofit

def nonprofit(request):
    if request.user.is_authenticated():
        list = Nonprofit.objects.filter(user=request.user)
        return {'nonprofit_list': list}
    return {}

def volunteer(request):
    if request.user.is_authenticated():
        try:
            return {'volunteer_session': Volunteer.objects.get(user=request.user)}
        except Volunteer.DoesNotExist:
            pass
    return {}

def site(request):
    return {'site': Site.objects.get_current()}
