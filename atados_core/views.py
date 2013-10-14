from django.contrib.auth.models import User
from django.core.mail import send_mail

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from atados_core.models import Nonprofit, Volunteer, Project, Availability, Cause, Skill, State, City, Suburb, Address, Donation, Work, Material, Role, Apply, Recommendation
from atados_core.serializers import UserSerializer, NonprofitSerializer, VolunteerSerializer, ProjectSerializer, CauseSerializer, SkillSerializer, AddressSerializer, StateSerializer, CitySerializer, SuburbSerializer, AvailabilitySerializer
from atados_core.permissions import IsOwnerOrReadOnly

import facepy as facebook
from provider.oauth2.views import AccessToken, Client


@api_view(['GET'])
def current_user(request, format=None):
  if request.user.is_authenticated():
    try:
      volunteer = Volunteer.objects.get(user=request.user)
    except:
     return  Response({"There was an error in our servers. Please contact us if the problem persists."}, status.HTTP_404_NOT_FOUND)

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
def facebook_auth(request, format=None):
  accessToken = request.DATA['accessToken']
  userID = request.DATA['userID']
  expiresIn = request.DATA['expiresIn']

  try:
    graph = facebook.GraphAPI(accessToken)
    me = graph.get("me")
  except facebook.FacepyError, e:
    return Response({"Could not talk to Facebook to log you in."}, status.HTTP_400_BAD_REQUEST)

  volunteer = Volunteer.objects.filter(facebook_uid=userID)

  if volunteer:
    volunteer = volunteer[0]
    user = volunteer.user
  else:
    user = User.objects.get(email=me['email'])

    try:
      volunteer = Volunteer.objects.get(user=user)
    except:
      user = User.objects.create_user(username=me['username'], email=me['email'])
      volunteer = Volunteer(user=user)

    if not user.first_name:
      user.first_name = me['first_name']
      user.save()
    if not user.last_name:
      user.last_name = me['last_name']
      user.save()
    
    # TODO(mpomarole): get photo later
    volunteer.facebook_uid = userID
    volunteer.facebook_access_token = accessToken
    volunteer.facebook_access_tolen_expires = expiresIn
    volunteer.save()

  if not volunteer: 
    return Response({"Could not get user through facebook login."}, status.HTTP_404_NOT_FOUND)
    
  client = Client.objects.get(id=1)
  token = AccessToken.objects.create(user=user, client=client)
  data = {
    'access_token': token.token,
    'user': VolunteerSerializer(volunteer).data
  }
  return Response(data, status.HTTP_200_OK)

@api_view(['POST'])
def logout(request, format=None):
  if not request.user.is_authenticated():
    return Response({"User not authenticated."}, status.HTTP_404_NOT_FOUND)
  else:
    token = AccessToken.objects.get(token=request.auth)
    token.delete()
    return Response({"User logged out."}, status.HTTP_200_OK)

@api_view(['PUT'])
def create_volunteer(request, format=None):
   username = request.DATA['username']
   email = request.DATA['email']
   password = request.DATA['password']
   try:
     user = User.objects.get(username=username, email=email)
   except User.DoesNotExist:
     user = User.objects.create_user(username, email, password)
   if Volunteer.objects.filter(user=user):
     return Response({'detail': 'Volunteer already exists.'}, status.HTTP_404_NOT_FOUND) 
   volunteer = Volunteer(user=user)
   volunteer.save()
   return Response({'detail': 'Volunteer succesfully created.'}, status.HTTP_200_OK) 
   # send activation email

@api_view(['POST'])
def password_reset(request, format=None):
  email = request.DATA['email']
  user = User.objects.get(email=email)
  password = User.objects.make_random_password()
  user.set_password(password)
  user.save()
  message = "Sua nova senha: "
  message += password
  message += ". Por favor entre na sua conta e mude para algo de sua preferencia. Qualquer duvida contate contato@atados.com.br."
  send_mail('Sua nova senha', message, 'contato@atados.com.br', [email])
  return Response({"Senha foi mandada"}, status.HTTP_200_OK)

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
  permission_classes = [IsAdminUser]

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
