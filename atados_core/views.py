import facepy as facebook
import json
import pytz                  
import urllib2                                       
from django.core.files import File                   
from django.core.files.temp import NamedTemporaryFile
from django.utils.encoding import iri_to_uri         
from django.utils import timezone
from datetime import datetime

from django.core.mail import send_mail
from django.http import Http404
from django.template.defaultfilters import slugify

from haystack.query import SearchQuerySet
from haystack.inputs import Clean, AutoQuery

from provider.oauth2.views import AccessToken, Client

from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from atados_core.models import Nonprofit, Volunteer, Project, Availability, Cause, Skill, State, City, Address, User, Apply, ApplyStatus, VolunteerResource, Role, Job, Work
from atados_core.serializers import UserSerializer, NonprofitSerializer, NonprofitSearchSerializer, VolunteerSerializer, VolunteerPublicSerializer, ProjectSerializer, ProjectSearchSerializer, CauseSerializer, SkillSerializer, AddressSerializer, StateSerializer, CitySerializer, AvailabilitySerializer, ApplySerializer, VolunteerProjectSerializer
from atados_core.permissions import IsOwnerOrReadOnly, IsNonprofit

@api_view(['GET'])
def current_user(request, format=None):
  if request.user.is_authenticated():
    request.user.last_login=timezone.now()
    request.user.save()
    try:
      return Response(VolunteerSerializer(request.user.volunteer).data)
    except:
      try:
        return Response(NonprofitSerializer(request.user.nonprofit).data)
      except:
        return  Response({"There was an error in our servers. Please contact us if the problem persists."}, status.HTTP_404_NOT_FOUND)

  return Response({"No user logged in."}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def check_slug(request, format=None):
  try:
    User.objects.get(slug=request.QUERY_PARAMS['slug'])
    return Response("Already exists.", status.HTTP_400_BAD_REQUEST)
  except User.DoesNotExist:
    return Response({"OK."}, status.HTTP_200_OK)

@api_view(['GET'])
def slug_role(request, format=None):
  try:
    user = User.objects.get(slug=request.QUERY_PARAMS['slug'])
    try:
      return Response({'type': Nonprofit.objects.get(user=user).get_type()}, status.HTTP_200_OK)
    except:
      return Response({'type': Volunteer.objects.get(user=user).get_type()}, status.HTTP_200_OK)
  except User.DoesNotExist:
    return Response({"Not found."}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def legacy_to_slug(request, type, format=None):
  try:
    uid = request.QUERY_PARAMS['uid']
    if type == 'nonprofit':
      slug = User.objects.get(legacy_uid=uid).slug
    if type == 'project':
      slug = Project.objects.get(legacy_nid=uid).slug
    return Response({'slug': slug}, status.HTTP_200_OK)
  except:
    return Response({"Not found."}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def check_project_slug(request, format=None):
  try:
    Project.objects.get(slug=request.QUERY_PARAMS['slug'])
    return Response("Already exists.", status.HTTP_400_BAD_REQUEST)
  except Project.DoesNotExist:
    return Response({"OK."}, status.HTTP_200_OK)

@api_view(['GET'])
def check_email(request, format=None):
  try:
    User.objects.get(email=request.QUERY_PARAMS['email'].split('?')[0])
    return Response("Already exists.", status.HTTP_400_BAD_REQUEST)
  except User.DoesNotExist:
    return Response({"OK."}, status.HTTP_200_OK)

@api_view(['POST'])
def facebook_auth(request, format=None):
  accessToken = request.DATA['accessToken']
  userID = request.DATA['userID']
  expiresIn = request.DATA['expiresIn']
  getPhoto = request.DATA.get('getPhoto', None)

  try:
    graph = facebook.GraphAPI(accessToken)
    me = graph.get("me")
  except facebook.FacepyError:
    return Response({"Could not talk to Facebook to log you in."}, status.HTTP_400_BAD_REQUEST)

  volunteer = Volunteer.objects.filter(facebook_uid=userID)

  if volunteer:
    volunteer = volunteer[0]
    if getPhoto:
      faceImage = graph.get("me/picture?redirect=0&height=200&type=normal&width=200")
      imgurl = iri_to_uri(faceImage['data']['url'])
      image = NamedTemporaryFile(delete=True)
      image.write(urllib2.urlopen(imgurl).read())
      image.flush()
      imgname = 'volunteer/%s/%s.jpg' % (volunteer.user.slug, volunteer.user.slug)
      volunteer.image.save(imgname, File(image))
      volunteer.save()
    user = volunteer.user
    user.last_login=timezone.now()
    user.save()
  else:
    try:
      user = User.objects.get(email=me['email'])
      volunteer = Volunteer.objects.get(user=user)
    except:
      try:
        slug = me['username']
      except:
        slug = slugify(me['name'])

      user = User.objects.create_user(slug=slug, email=me['email'])
      volunteer = Volunteer(user=user)

    user.last_login=timezone.now()
    user.name = me['name']
    user.save()
    
    faceImage = graph.get("me/picture?redirect=0&height=200&type=normal&width=200")
    imgurl = iri_to_uri(faceImage['data']['url'])
    image = NamedTemporaryFile(delete=True)
    image.write(urllib2.urlopen(imgurl).read())
    image.flush()
    imgname = 'volunteer/%s/%s.jpg' % (volunteer.user.slug, volunteer.user.slug)
    volunteer.image.save(imgname, File(image))
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
    return Response(UserSerializer(request.user).data, status.HTTP_200_OK)

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

@api_view(['POST'])
def create_nonprofit(request, format=None):
  obj = json.loads(request.DATA['nonprofit'])
  email = obj['user']['email']

  obja = obj['address']
  address = Address()
  address.zipcode = obja['zipcode'][0:9]
  address.addressline = obja['addressline']
  address.addressline2 = obja.get('addressline2')
  address.addressnumber = obja['addressnumber'][0:9]
  address.neighborhood = obja['neighborhood']
  address.city = City.objects.get(id=obja['city']['id'])
  address.save()

  try:
   user = User.objects.get(email=email)
  except User.DoesNotExist:
   password = obj['user']['password']
   user = User.objects.create_user(email, password, slug=obj['user']['slug'])
   user.name = obj['user']['name']
   user.hidden_address = obj['hidden_address']
   user.address = address
   user.save()

  if Nonprofit.objects.filter(user=user):
   return Response({'detail': 'Nonprofit already exists.'}, status.HTTP_404_NOT_FOUND) 

  
  FACEBOOK_KEY = 'facebook_page'
  GOOGLE_KEY = 'google_page'
  TWITTER_KEY = 'twitter_handle'

  nonprofit = Nonprofit(user=user)
  nonprofit.name = obj['name']
  nonprofit.details = obj['details']
  nonprofit.description = obj['description']
  nonprofit.phone = obj['phone']
  nonprofit.save()

  causes = obj['causes']
  for c in causes:
    nonprofit.causes.add(Cause.objects.get(name=c['name']))

  if FACEBOOK_KEY in obj:
   nonprofit.facebook_page = obj[FACEBOOK_KEY]
  if GOOGLE_KEY in obj:
   nonprofit.google_page = obj[GOOGLE_KEY]
  if TWITTER_KEY in obj:
   nonprofit.twitter_handle = obj[TWITTER_KEY]

  nonprofit.image = request.FILES.get('image')
  nonprofit.cover = request.FILES.get('cover')
  nonprofit.save()

  return Response({'detail': 'Nonprofit succesfully created.'}, status.HTTP_200_OK) 

@api_view(['GET'])
def create_project_slug(request, format=None):
  name = request.QUERY_PARAMS.get('name', None);
  if name:
    slug = slugify(name)[0:46]                            
    append = ''                                           
    i = 0                                                 
    while len(Project.objects.filter(slug=slug + append)):
      i += 1                                            
      append = '-' + str(i)                             
      return Response(slug + append, status.HTTP_200_OK) 
    return Response({'slug': slug}, status.HTTP_200_OK) 

  return Response({'error': ':('}, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_project(request, format=None):
  if not request.user.is_authenticated() or not request.user.nonprofit:
    return Response({"User not authenticated."}, status.HTTP_403_FORBIDDEN)

  obj = request.DATA['project'];
  project = Project()
  try:
    project.name = obj['name']
    project.nonprofit = Nonprofit.objects.get(id=obj['nonprofit'])
    project.slug = obj['slug']
    project.details = obj['details']
    project.description = obj['description']
    project.facebook_event = obj['facebook_event']
    project.responsible = obj['responsible']
    project.phone = obj['phone']
    project.email = obj['email']
    project.save()
    obja = obj['address']
    address = Address()
    address.addressline = obja['addressline']
    address.addressline2 = obja['addressline2']
    address.addressnumber = obja['addressnumber']
    address.neighborhood = obja['neighborhood']
    address.zipcode = obja['zipcode']
    address.city = City.objects.get(id=obja['city']['id'])
    address.save()
    project.address = address
    project.image = request.FILES.get('image')

    roles = obj['roles']
    for r in roles:
      role = Role()
      role.name = r['name']
      role.prerequisites = r['prerequisites']
      role.details = r['details']
      role.vacancies = r['vacancies']
      role.save()
      project.roles.add(role)

    skills = obj['skills']
    for s in skills:
      project.skills.add(Skill.objects.get(name=s['name']))

    causes = obj['causes']
    for c in causes:
      project.causes.add(Cause.objects.get(name=c['name']))

    if obj.get('work', None):
      work =  Work()
      work.project = project
      work.weekly_hours = obj['work']['weekly_hours']
      work.can_be_done_remotely = obj['work']['can_be_done_remotely']
      availabilities = obj['work']['availabilities']
      for a in availabilities:
        availability = Availability()
        availability.weekday = a['weekday']
        availability.period = a['period']
        availability.save()
        work.availabilities.add(availability)
      work.save()
    elif obj.get('job', None):
      job = Job()
      job.project = project
      job.start_date = datetime.utcfromtimestamp(obj['job']['start_date']/1000).replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
      job.end_date = datetime.utcfromtimestamp(obj['job']['end_date']/1000).replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
      job.save()

    project.save()
  except Exception as inst:
    print inst
    return Response({'detail': 'Something.'}, status.HTTP_400_BAD_REQUEST) 

  return Response({'detail': 'Project succesfully created.'}, status.HTTP_201_CREATED) 

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

@api_view(['POST'])
def send_volunteer_email_to_nonprofit(request, format=None):
  message = request.DATA['message'].encode('utf-8').strip()
  nonprofitEmail = request.DATA['nonprofit']
  volunteerEmail = request.DATA['volunteer']
  if not volunteerEmail or not nonprofitEmail or not message:
    return Response({"Not enough information."}, status.HTTP_400_BAD_REQUEST)
  print 'Sending %s from %s to %s' % (message, volunteerEmail, nonprofitEmail)
  send_mail('Atados Voluntario Atado', message, volunteerEmail, [nonprofitEmail])
  return Response({"Email was sent."}, status.HTTP_200_OK)

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

@api_view(['POST'])
def upload_nonprofit_profile_image(request, format=None):
  if request.user.is_authenticated() and request.user.nonprofit:
    nonprofit = request.user.nonprofit
    nonprofit.image = request.FILES.get('file')
    nonprofit.save()
    return Response({"file": nonprofit.get_image_url()}, status.HTTP_200_OK)
  return Response({"Not logged in or not nonprofit."}, status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def upload_nonprofit_cover_image(request, format=None):
  if request.user.is_authenticated() and request.user.nonprofit:
    nonprofit = request.user.nonprofit
    nonprofit.cover = request.FILES.get('file')
    nonprofit.save()
    return Response({"file": nonprofit.get_cover_url()}, status.HTTP_200_OK)
  return Response({"Not logged in or not nonprofit."}, status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def numbers(request, format=None):
  numbers = {}
  numbers['projects'] = Project.objects.filter(closed=False, published=True).count()
  numbers['volunteers'] = Volunteer.objects.count()
  numbers['nonprofits'] = Nonprofit.objects.filter(published=True).count()
  return Response(numbers, status.HTTP_200_OK)

@api_view(['GET'])
def is_volunteer_to_nonprofit(request, format=None):
  if request.user.is_authenticated():
    volunteer = Volunteer.objects.get(user=request.user)
    nonprofit = request.QUERY_PARAMS['nonprofit']
    if nonprofit:
      if volunteer.nonprofit_set.filter(id=nonprofit).exists():
        return Response({"YES"}, status.HTTP_200_OK)
      return Response({"NO"}, status.HTTP_200_OK)
  return Response({"NO"}, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def set_volunteer_to_nonprofit(request, format=None):
  if request.user.is_authenticated():
    volunteer = Volunteer.objects.get(user=request.user)
    nonprofit = request.DATA['nonprofit']
    if nonprofit:
      if volunteer.nonprofit_set.filter(id=nonprofit).exists():
        nonprofit = Nonprofit.objects.get(id=nonprofit)
        nonprofit.volunteers.remove(volunteer)
        return Response({"Removed"}, status.HTTP_200_OK)
      else:
        nonprofit = Nonprofit.objects.get(id=nonprofit)
        nonprofit.volunteers.add(volunteer)
        return Response({"Added"}, status.HTTP_200_OK)
  return Response({"Could not find nonprofit or volunteer"}, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def apply_volunteer_to_project(request, format=None):
  if request.user.is_authenticated():
    volunteer = Volunteer.objects.get(user=request.user)
    project = Project.objects.get(id=request.DATA['project'])
    if project:
      try:
        # If apply exists, then cancel it 
        apply = Apply.objects.get(project=project, volunteer=volunteer)
        if not apply.canceled:
          apply.canceled = True
          apply.status = ApplyStatus.objects.get(id=3) # Desistente
          apply.save()
          return Response({"Canceled"}, status.HTTP_200_OK)
        else:
          apply.canceled = False
          apply.status = ApplyStatus.objects.get(id=2) # Candidato 
          apply.save()
          return Response({"Applied"}, status.HTTP_200_OK)
      except:
        apply = Apply()
        apply.project = project
        apply.volunteer = volunteer
        apply.status = ApplyStatus.objects.get(id=2) # Candidato 
        apply.save()
        return Response({"Applied"}, status.HTTP_200_OK)

  return Response({"Could not find project or volunteer"}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def has_volunteer_applied(request, format=None):
  if request.user.is_authenticated():
    volunteer = Volunteer.objects.get(user=request.user)
    project = request.QUERY_PARAMS['project']
    if project and volunteer:
      try:
        apply = Apply.objects.get(project=project, volunteer=volunteer)
        if apply.canceled:
          return Response({"NO"}, status.HTTP_200_OK)
        return Response({"YES"}, status.HTTP_200_OK)
      except:
        return Response({"NO"}, status.HTTP_200_OK)
  return Response({"NO"}, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def change_volunteer_status(request, format=None):
  if request.user.is_authenticated():
    try:
      project = request.DATA['project']
      volunteer = request.DATA['volunteer']
      s =  request.DATA['volunteerStatus']
      project = Project.objects.get(slug=project)
      volunteer = User.objects.get(email=volunteer).volunteer
      a = Apply.objects.get(volunteer=volunteer, project=project)
      a.status = ApplyStatus.objects.get(name=s)
      a.save()
      return Response({"OK"}, status.HTTP_200_OK)
    except Exception:
      return Response({"Some error with the parameters you passed."}, status.HTTP_400_BAD_REQUEST)
  return Response({"Some error with the parameters you passed."}, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def clone_project(request, project_slug, format=None):
  def new_slug(slug):
    append = '-2'
    i = 2
    while (Project.objects.filter(slug=slug + append).exists()):
        i += 1
        append = '-' + str(i)
    return slug + append
    
  if request.user.is_authenticated():
    try:
      project = Project.objects.get(slug=project_slug)
      project.pk = None
      project.slug = new_slug(project.slug)
      address = project.address
      address.pk = None
      address.save()
      project.address = address
      project.published = False
      project.save()
      return Response(ProjectSerializer(project).data, status.HTTP_200_OK)
    except Exception as inst:
      print inst
      return Response({"Some error cloning the project."}, status.HTTP_400_BAD_REQUEST)
  return Response({"Some error cloning the project."}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def export_project_csv(request, project_slug, format=None):
  if request.user.is_authenticated():
    try:
      project = Project.objects.get(slug=project_slug)
      data = VolunteerResource().export(project.get_volunteers()).csv
      return Response({'volunteers': data}, status.HTTP_200_OK)
    except Exception as inst:
      print inst
      return Response({"Some error with export csv of project."}, status.HTTP_400_BAD_REQUEST)
  return Response({"Some error with export csv of project."}, status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAdminUser]
  lookup_field = 'slug'

class NonprofitViewSet(viewsets.ModelViewSet):
  queryset = Nonprofit.objects.filter(deleted=False)
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
  serializer_class = ProjectSearchSerializer
  permission_classes = [AllowAny]

  def get_queryset(self):
    params = self.request.GET
    query = params.get('query', None)
    cause = params.get('cause', None)
    skill = params.get('skill', None)
    city = params.get('city', None)
    nonprofit = params.get('nonprofit', None)
    if nonprofit:
      nonprofit = Nonprofit.objects.get(user__slug=nonprofit)
      queryset = Project.objects.filter(nonprofit=nonprofit)
    else:
        queryset = SearchQuerySet()
    queryset = queryset.filter(causes=cause) if cause else queryset
    queryset = queryset.filter(skills=skill) if skill else queryset
    queryset = queryset.filter(city=city) if city else queryset
    queryset = queryset.filter(content=AutoQuery(query.lower())) if query else queryset

    highlighted = True if params.get('highlighted') == 'true' else False
    if highlighted:
      return Project.objects.filter(pk__in=[ r.pk for r in queryset ], closed=False, published=True).order_by('-highlighted')
    else:
      return Project.objects.filter(pk__in=[ r.pk for r in queryset ], closed=False, published=True).order_by('?')

class NonprofitList(generics.ListAPIView):
  serializer_class = NonprofitSearchSerializer
  permission_classes = [AllowAny]

  def get_queryset(self):
    params = self.request.GET
    query = params.get('query', None)
    cause = params.get('cause', None)
    city = params.get('city', None)
    queryset = SearchQuerySet()
    queryset = SearchQuerySet().filter(causes=cause) if cause else queryset
    queryset = queryset.filter(city=city) if city else queryset
    queryset = queryset.filter(content=Clean(query)) if query else queryset
    results = [ r.pk for r in queryset ]
    highlighted = True if params.get('highlighted') == 'true' else False
    if highlighted:
      return Nonprofit.objects.filter(pk__in=results).order_by('-highlighted')
    else:
      return Nonprofit.objects.filter(pk__in=results).order_by('?')


class VolunteerProjectList(generics.ListAPIView):
  serializer_class = VolunteerProjectSerializer
  permission_classes = (IsNonprofit, )

  def get_queryset(self):
    project_slug = self.kwargs.get('project_slug', None)
    applies = Apply.objects.filter(project__slug=project_slug)
    ids = applies.values_list('volunteer', flat=True)
    volunteers = Volunteer.objects.filter(id__in=ids)
    return volunteers

class VolunteerPublicViewSet(viewsets.ModelViewSet):
  queryset = Volunteer.objects.all()
  serializer_class = VolunteerPublicSerializer
  lookup_field = 'slug'

  def get_object(self):
    try:
      volunteer = self.get_queryset().get(user__slug=self.kwargs['slug'])
      volunteer.slug = volunteer.user.slug
      return volunteer
    except:
      raise Http404

class VolunteerViewSet(viewsets.ModelViewSet):
  queryset = Volunteer.objects.all()
  serializer_class = VolunteerSerializer
  lookup_field = 'slug'

  def get_object(self):
    try:
      volunteer = self.get_queryset().get(user__slug=self.kwargs['slug'])
      volunteer.slug = volunteer.user.slug
      if self.request.user == volunteer.user:
        return volunteer
    except:
      raise Http404

class ProjectViewSet(viewsets.ModelViewSet):
  queryset = Project.objects.filter(deleted=False)
  serializer_class = ProjectSerializer
  permissions_classes = [IsNonprofit]
  lookup_field = 'slug'

class ApplyViewSet(viewsets.ModelViewSet):
  queryset = Apply.objects.all()
  serializer_class = ApplySerializer
  permissions_classes = [IsOwnerOrReadOnly]

class ApplyList(generics.ListAPIView):
  serializer_class = ApplySerializer
  permission_classes = [IsNonprofit]

  def get_queryset(self):
    project_slug = self.request.QUERY_PARAMS['project_slug']
    volunteer_slug = self.request.QUERY_PARAMS['volunteer_slug']
    applies = Apply.objects.filter(project__slug=project_slug, volunteer__user__slug=volunteer_slug).distinct()
    return applies

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

class StateViewSet(viewsets.ReadOnlyModelViewSet):
  model = State
  serializer_class = StateSerializer
  permission_classes = [AllowAny]
  
  def get_queryset(self):
    return State.objects.all().order_by('id')

class CityViewSet(viewsets.ReadOnlyModelViewSet):
  model = City
  serializer_class = CitySerializer
  permission_classes = [AllowAny]

  def get_queryset(self):
    try:
      return City.objects.filter(state_id=self.request.QUERY_PARAMS['state']).order_by('name')
    except:
      return City.objects.all().order_by('-active')

class AvailabilityViewSet(viewsets.ModelViewSet):
  queryset = Availability.objects.all()
  serializer_class = AvailabilitySerializer
