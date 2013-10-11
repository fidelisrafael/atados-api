from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from atados_core.models import Nonprofit, Volunteer, Project, Availability, Cause, Skill, State, City, Suburb, Address, Donation, Work, Material, Role, Apply, Recommendation
from atados_core.serializers import UserSerializer, NonprofitSerializer, VolunteerSerializer, ProjectSerializer, CauseSerializer, SkillSerializer, AddressSerializer, StateSerializer, CitySerializer, SuburbSerializer, AvailabilitySerializer
from atados_core.permissions import IsOwnerOrReadOnly

# Views the API need to provide
#
# 1. For unauthenticated/public users to view
#   - View a list of all open Projects
#   - View a list of all approved Nonprofits
#   - View a list of all approved 
#
# 2. Authenticated Volunteer
#   - update his Volunteer Profile
#   - view all open Projects
#   - view all Projects he has under his profile
#   - view all Nonprofits he has associations with 
#
# 3. Authenticated Nonprofit
#   - update Nonprofit Profile
#     - open projects
#     - closed projects
#   - create a Project
#   - view all open projects by all nonprofits
#   - view all open projects still on going for the non

@api_view(['GET'])
def current_user(request, format=None):
  if request.user.is_authenticated():
    volunteer = Volunteer.objects.get(user=request.user)
    if volunteer:
      return Response(VolunteerSerializer(volunteer).data)
    else:
      nonprofit = Nonprofit.objects.get(user=request.user)
      return Response(NonprofitSerializer(nonprofit).data)
  else:
    content = {'detail': 'No user logged in.'}
    return Response(content, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request, format=None):
  if not request.user.is_authenticated():
    return Response({"User already logged out"}, status.HTTP_404_NOT_FOUND)
  else:
    # TODO actually log out the user
    return Response({"User logged out."}, status.HTTP_HTTP_200_OK)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
  permission_classes = [IsAuthenticated]
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def get_queryset(self):
    """
    This view should return a list of all the purchases for the currently authenticated user.
    """
    user = self.request.user
    if (user.is_authenticated()):
      return Volunteer.objects.filter(user=user)
    else:
      return Volunteer.objects.all()

class NonprofitViewSet(viewsets.ModelViewSet):
  queryset = Nonprofit.objects.all()
  serializer_class = NonprofitSerializer
  permission_classes = [IsOwnerOrReadOnly]

class VolunteerViewSet(viewsets.ModelViewSet):
  queryset = Volunteer.objects.all()
  serializer_class = VolunteerSerializer
  permission_classes = [IsOwnerOrReadOnly]

class ProjectViewSet(viewsets.ModelViewSet):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer
  permissions_classes = [IsOwnerOrReadOnly]
 
class CauseViewSet(viewsets.ModelViewSet):
  queryset = Cause.objects.all()
  serializer_class = CauseSerializer

class SkillViewSet(viewsets.ModelViewSet):
  queryset = Skill.objects.all()
  serializer_class = SkillSerializer
 
class AddressViewSet(viewsets.ModelViewSet):
  queryset = Address.objects.all()
  serializer_class = AddressSerializer

class StateViewSet(viewsets.ModelViewSet):
  queryset = State.objects.all()
  serializer_class = StateSerializer

class CityViewSet(viewsets.ModelViewSet):
  queryset = City.objects.all()
  serializer_class = CitySerializer

class SuburbViewSet(viewsets.ModelViewSet):
  queryset = Suburb.objects.all()
  serializer_class = SuburbSerializer

class AvailabilityViewSet(viewsets.ModelViewSet):
  queryset = Availability.objects.all()
  serializer_class = AvailabilitySerializer
