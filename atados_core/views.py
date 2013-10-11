from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from atados_core.models import Nonprofit, Volunteer, Project, Availability, Cause, Skill, State, City, Suburb, Address, Donation, Work, Material, Role, Apply, Recommendation
from atados_core.serializers import UserSerializer, NonprofitSerializer, VolunteerSerializer, ProjectSerializer, CauseSerializer, SkillSerializer, AddressSerializer, StateSerializer, CitySerializer, SuburbSerializer, AvailabilitySerializer
from atados_core.permissions import IsOwnerOrReadOnly

from allauth.account.forms import LoginForm

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

@api_view(['POST'])
def login(request, format=None):
  form = LoginForm({'login': request.DATA['username'], 'password': request.DATA['password'], 'remember': request.DATA['remember']})
  form.login(request, None)
  if form.is_valid():
    print "is valid!"
  else:
    print "isnot"
  return Response("what", status.HTTP_200_OK)

@api_view(['GET'])
def current_user(request, format=None):
  print request.user
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

@api_view(['GET'])
def check_username(request, format=None):
  try:
    user = User.objects.get(username=request.QUERY_PARAMS['username'])
    return Response("Already exists.", status.HTTP_400_BAD_REQUEST)
  except User.DoesNotExist:
    return Response({"OK."}, status.HTTP_200_OK)

@api_view(['GET'])
def check_email(request, format=None):
  try:
    user = User.objects.get(email=request.QUERY_PARAMS['email'])
    return Response("Already exists.", status.HTTP_400_BAD_REQUEST)
  except User.DoesNotExist:
    return Response({"OK."}, status.HTTP_200_OK)


@api_view(['POST'])
def logout(request, format=None):
  if not request.user.is_authenticated():
    return Response({"User already logged out"}, status.HTTP_404_NOT_FOUND)
  else:
    # TODO actually log out the user
    return Response({"User logged out."}, status.HTTP_200_OK)

@api_view(['PUT'])
def create_volunteer(request, format=None):
   password = request.DATA['username']
   password = request.DATA['email']
   password = request.DATA['password']
   try:
     user = User.objects.get(username=username, email=email)
   except Person.DoesNotExist:
     user = User.objects.create_user(username, email, password)
     user.save()
   Volunteer.objects.create_volutneer
   # send activation email

@api_view(['PUT'])
def create_nonprofit(request, format=None):
  pass # TODO

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  lookup_field = 'username'
  permission_classes = [IsAdminUser]

class NonprofitViewSet(viewsets.ModelViewSet):
  queryset = Nonprofit.objects.all()
  serializer_class = NonprofitSerializer
  permission_classes = [IsOwnerOrReadOnly]

class VolunteerViewSet(viewsets.ModelViewSet):
  queryset = Volunteer.objects.all()
  serializer_class = VolunteerSerializer
  lookup_field = 'username'
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
