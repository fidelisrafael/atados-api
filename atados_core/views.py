import facepy as facebook

from django.core.mail import send_mail
from django.http import Http404
from django.template.defaultfilters import slugify

from haystack.query import SearchQuerySet
from provider.oauth2.views import AccessToken, Client

from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from atados_core.models import Nonprofit, Volunteer, Project, Availability, Cause, Skill, State, City, Suburb, Address, Role, User
from atados_core.serializers import UserSerializer, NonprofitSerializer, VolunteerSerializer, ProjectSerializer, CauseSerializer, SkillSerializer, AddressSerializer, StateSerializer, CitySerializer, SuburbSerializer, AvailabilitySerializer, WorkSerializer, RoleSerializer
from atados_core.permissions import IsOwnerOrReadOnly

@api_view(['GET'])
def current_user(request, format=None):
  if request.user.is_authenticated():
    try:
      v = VolunteerSerializer(request.user.volunteer)
      return Response(v.data)
    except:
      try:
        return Response(NonprofitSerializer(request.user.nonprofit).data)
      except Exception as inst:
        print inst
        return  Response({"There was an error in our servers. Please contact us if the problem persists."}, status.HTTP_404_NOT_FOUND)

  return Response({"No user logged in."}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def check_slug(request, format=None):
  try:
    user = User.objects.get(slug=request.QUERY_PARAMS['slug'])
    return Response("Already exists.", status.HTTP_400_BAD_REQUEST)
  except User.DoesNotExist:
    return Response({"OK."}, status.HTTP_200_OK)

@api_view(['GET'])
def check_project_slug(request, format=None):
  try:
    project = Project.objects.get(slug=request.QUERY_PARAMS['slug'])
    return Response("Already exists.", status.HTTP_400_BAD_REQUEST)
  except Project.DoesNotExist:
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
    try:
      user = User.objects.get(email=me['email'])
      volunteer = Volunteer.objects.get(user=user)
    except:
      try:
        slug = me['username']
      except:
        slug = slugify(me['first_name'] + me['last_name'])

      user = User.objects.create_user(slug=slug, email=me['email'])
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
    volunteer.facebook_access_token_expires = expiresIn
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

@api_view(['POST'])
def create_volunteer(request, format=None):
   slug = request.DATA['slug']
   email = request.DATA['email']
   password = request.DATA['password']
   try:
     user = User.objects.get(email=email)
   except User.DoesNotExist:
     user = User.objects.create_user(email, password, slug=slug)

   if Volunteer.objects.filter(user=user):
     return Response({'detail': 'Volunteer already exists.'}, status.HTTP_404_NOT_FOUND) 
   volunteer = Volunteer(user=user)
   volunteer.save()
   return Response({'detail': 'Volunteer succesfully created.'}, status.HTTP_201_CREATED) 
   # TODO send activation email

@api_view(['POST'])
def create_nonprofit(request, format=None):
   obj = request.DATA
   slug = obj['user']['slug']
   email = obj['user']['email']

   try:
     user = User.objects.get(email=email)
   except User.DoesNotExist:
     password = obj['user']['password']
     user = User.objects.create_user(email, password, slug=obj['user']['slug'])
     user.first_name = obj['user']['first_name']
     user.last_name = obj['user']['last_name']
     user.save()

   if Nonprofit.objects.filter(user=user):
     return Response({'detail': 'Nonprofit already exists.'}, status.HTTP_404_NOT_FOUND) 

   obja = obj['address']
   address = Address()
   address.zipcode = obja['zipcode']
   address.addressline = obja['addressline']
   address.addressline2 = obja.get('addressline2')
   address.addressnumber = obja['addressnumber']
   address.neighborhood = obja['neighborhood']
   address.suburb = Suburb.objects.get(id=obja['suburbs']['id'])
   address.save()

   FACEBOOK_KEY = 'facebook_page'
   GOOGLE_KEY = 'google_page'
   TWITTER_KEY = 'twitter_handle'

   nonprofit = Nonprofit(user=user)
   nonprofit.address = address
   nonprofit.name = obj['name']
   nonprofit.details = obj['details']
   nonprofit.description = obj['description']
   nonprofit.slug = obj['slug']
   nonprofit.phone = obj['phone']

   if FACEBOOK_KEY in obj:
     nonprofit.facebook_page = obj[FACEBOOK_KEY]
   if GOOGLE_KEY in obj:
     nonprofit.google_page = obj[GOOGLE_KEY]
   if TWITTER_KEY in obj:
     nonprofit.twitter_handle = obj[TWITTER_KEY]

   nonprofit.save()

   return Response({'detail': 'Nonprofit succesfully created.'}, status.HTTP_200_OK) 
   # TODO send activation email
   # TODO send  email to administradors to accept this Nonprofit and remove it from moderation

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
  return Response({"Password was sent."}, status.HTTP_200_OK)

@api_view(['PUT'])
def change_password(request, format=None):
  email = request.DATA['email']
  user = User.objects.get(email=email)
  password = request.DATA['password']
  if email and password and user:
    user.set_password(password)
    user.save()
    return Response({"Password set successfuly"}, status.HTTP_200_OK)
  else:
    return Response({"There was a problem setting your password"}, status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def upload_volunteer_image(request, format=None):
  if request.user.is_authenticated():
    volunteer = Volunteer.objects.get(user=request.user)
    volunteer.image = request.FILES.get('file')
    volunteer.save()
    return Response({"file": volunteer.get_image_url()}, status.HTTP_200_OK)
  return Response({"Not logged in."}, status.HTTP_403_FORBIDDEN)

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAdminUser]
  lookup_field = 'slug'

class NonprofitViewSet(viewsets.ModelViewSet):
  queryset = Nonprofit.objects.all()
  serializer_class = NonprofitSerializer
  permission_classes = [IsOwnerOrReadOnly]
  lookup_field = 'slug'

  def get_object(self):
    try:
      nonprofit = self.get_queryset().get(user__slug=self.kwargs['slug'])
      nonprofit.slug = nonprofit.user.slug
      self.check_object_permissions(self.request, nonprofit)
      return nonprofit
    except:
      raise Http404

class ProjectList(generics.ListAPIView):
  serializer_class = ProjectSerializer
  permission_classes = [AllowAny]

  def get_queryset(self):
    params = self.request.GET
    query = params.get('query', None)
    queryset = SearchQuerySet().filter(content=query).models(Project) if query else SearchQuerySet().all().models(Project)
    results = [ r.pk for r in queryset ]
    return Project.objects.filter(pk__in=results)

class NonprofitList(generics.ListAPIView):
  serializer_class = NonprofitSerializer
  permission_classes = [AllowAny]

  def get_queryset(self):
    params = self.request.GET
    query = params.get('query', None)
    queryset = SearchQuerySet().filter(content=query).models(Nonprofit) if query else SearchQuerySet().all().models(Nonprofit)
    results = [ r.pk for r in queryset ]
    return Nonprofit.objects.filter(pk__in=results)

class VolunteerList(generics.ListAPIView):
  serializer_class = VolunteerSerializer
  permission_classes = [AllowAny]

  def get_queryset(self):
    params = self.request.GET
    query = params.get('query', None)
    queryset = SearchQuerySet().filter(content=query).models(Volunteer) if query else SearchQuerySet().all().models(Nonprofit)
    results = [ r.pk for r in queryset ]
    return Nonprofit.objects.filter(pk__in=results)

class VolunteerViewSet(viewsets.ModelViewSet):
  queryset = Volunteer.objects.all()
  serializer_class = VolunteerSerializer
  permission_classes = [IsOwnerOrReadOnly]
  lookup_field = 'slug'

  def get_object(self):
    try:
      volunteer = self.get_queryset().get(user__slug=self.kwargs['slug'])
      volunteer.slug = volunteer.user.slug
      self.check_object_permissions(self.request, volunteer)
      return volunteer
    except:
      raise Http404

class ProjectViewSet(viewsets.ModelViewSet):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer
  permissions_classes = [IsOwnerOrReadOnly]
  lookup_field = 'slug'

class RoleViewSet(viewsets.ModelViewSet):
  queryset = Role.objects.all()
  serializer_class = RoleSerializer
  permissions_classes = [IsOwnerOrReadOnly]

class CauseViewSet(viewsets.ModelViewSet):
  queryset = Cause.objects.all()
  serializer_class = CauseSerializer
  permission_classes = [AllowAny]
  lookup_field = 'id'

class SkillViewSet(viewsets.ModelViewSet):
  queryset = Skill.objects.all()
  serializer_class = SkillSerializer
  permission_classes = [AllowAny]
  lookup_field = 'id'
 
class AddressViewSet(viewsets.ModelViewSet):
  queryset = Address.objects.all()
  serializer_class = AddressSerializer
  permission_classes = (IsOwnerOrReadOnly, IsAdminUser)

class StateViewSet(viewsets.ModelViewSet):
  queryset = State.objects.all()
  serializer_class = StateSerializer
  permission_classes = [AllowAny]

class CityViewSet(viewsets.ModelViewSet):
  queryset = City.objects.filter(active=True)
  serializer_class = CitySerializer
  permission_classes = [AllowAny]

class SuburbViewSet(viewsets.ModelViewSet):
  queryset = Suburb.objects.all()
  serializer_class = SuburbSerializer
  permission_classes = [AllowAny]

class AvailabilityViewSet(viewsets.ModelViewSet):
  queryset = Availability.objects.all()
  serializer_class = AvailabilitySerializer
