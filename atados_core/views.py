# -*- coding: utf-8 -*-

import boto
import facepy as facebook
import json
import pytz
import sys
import urllib2

from atados_core.models import Nonprofit, Volunteer, Project, Availability, Cause, Skill, State, City, Address, User, Apply, ApplyStatus, VolunteerResource, Role, Job, Work
from atados_core.permissions import IsOwnerOrReadOnly, IsNonprofit
from atados_core.serializers import UserSerializer, NonprofitSerializer, NonprofitSearchSerializer, VolunteerSerializer, VolunteerPublicSerializer, ProjectSerializer, ProjectSearchSerializer, CauseSerializer, SkillSerializer, AddressSerializer, StateSerializer, CitySerializer, AvailabilitySerializer, ApplySerializer, VolunteerProjectSerializer, JobSerializer, WorkSerializer, ProjectMapSerializer, NonprofitMapSerializer
from atados_core.tasks import send_email_to_volunteer_after_4_weeks_of_apply, send_email_to_volunteer_3_days_before_pontual

from datetime import datetime
from datetime import timedelta

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.mail import EmailMultiAlternatives
from django.http import Http404
from django.template import Context
from django.template.defaultfilters import slugify
from django.template.loader import get_template
from django.utils import timezone
from django.utils.encoding import iri_to_uri
from django.views.decorators.cache import cache_control

from haystack.query import SearchQuerySet

from provider.oauth2.views import AccessToken, Client

from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

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
      except Exception as e:
        print "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
        return  Response({"There was an error in our servers. Please contact us if the problem persists."}, status.HTTP_404_NOT_FOUND)

  return Response({"No user logged in."}, status.HTTP_400_BAD_REQUEST)

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
def check_slug(request, format=None):
  try:
    User.objects.get(slug=request.QUERY_PARAMS['slug'])
    return Response({"alreadyUsed": True}, status.HTTP_200_OK)
  except User.DoesNotExist:
    return Response({"alreadyUsed": False}, status.HTTP_200_OK)

@api_view(['GET'])
def check_email(request, format=None):
  try:
    User.objects.get(email=request.QUERY_PARAMS['email'].split('?')[0])
    return Response({"alreadyUsed": True}, status.HTTP_200_OK)
  except User.DoesNotExist:
    return Response({"alreadyUsed": False}, status.HTTP_200_OK)

@api_view(['POST'])
def facebook_auth(request, format=None):
  accessToken = request.DATA['accessToken']
  userID = request.DATA['userID']
  expiresIn = request.DATA['expiresIn']
  getPhoto = request.DATA.get('getPhoto', None)

  try:
    graph = facebook.GraphAPI(accessToken)
    me = graph.get("me")
  except facebook.FacepyError as e:
    print "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
    return Response({"We don't have permissions to log in the user."}, status.HTTP_403_FORBIDDEN)

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
      email = me.get('email', None)
      name = me.get('name', None)
      if name:
        slug = slugify(name)
      elif email:
        slug = slugify(email)
      else:
        return Response({"Could not creata slug for account."}, status.HTTP_400_BAD_REQUEST)

      user = User.objects.create_user(slug=slug, email=email, password="facebook")
      volunteer = Volunteer(user=user)

      try:
        # Sending welcome email on facebook signup
        plaintext = get_template('email/volunteerFacebookSignup.txt')
        htmly     = get_template('email/volunteerFacebookSignup.html')
        d = Context({ 'name': name })
        subject, from_email, to = 'Seja bem vindo ao Atados', 'contato@atados.com.br', email
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
      except:
        pass

    user.last_login=timezone.now()
    user.name = me.get('name', None)
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
    return Response({'detail': 'User already exists.'}, status.HTTP_404_NOT_FOUND)
  except User.DoesNotExist:
    site = request.META.get('HTTP_ORIGIN', 'https://www.atados.com.br')
    user = User.objects.create_user(email, password, slug=slug, site=site)
    # Sending welcome email on email signup
    plaintext = get_template('email/volunteerSignup.txt')
    htmly     = get_template('email/volunteerSignup.html')
    subject   = u"Seja bem vindo ao Atados"
    d = Context({ 'name': user.name })
    from_email, to = 'contato@atados.com.br', user.email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
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
   user.phone = obj['phone']
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

  # Sending welcome email on nonprofit signup
  plaintext = get_template('email/nonprofitSignup.txt')
  htmly     = get_template('email/nonprofitSignup.html')
  d = Context()
  subject, from_email, to = 'Cadastro no Atados enviado com sucesso!', 'contato@atados.com.br', nonprofit.user.email
  text_content = plaintext.render(d)
  html_content = htmly.render(d)
  msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
  msg.attach_alternative(html_content, "text/html")
  msg.send()

  return Response({'detail': 'Nonprofit succesfully created.'}, status.HTTP_200_OK)

def create_project_slug(name):
  if name:
    slug = slugify(name)[0:99]
    append = ''
    i = 0

    query = Project.objects.filter(slug=slug + append)
    while query.count() > 0:
      i += 1
      append = '-' + str(i)
      query = Project.objects.filter(slug=slug + append)
    return slug + append

@api_view(['POST'])
def create_project(request, format=None):
  # Need a nonprofit user
  try:
    request.user.nonprofit
  except Exception as e:
    error = "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
    return Response({"User not authenticated. " + error}, status.HTTP_403_FORBIDDEN)

  try:
    obj = json.loads(request.DATA['project'])
  except:
    obj = request.DATA['project']

  project = Project()
  try:
    # Getting required field
    project.nonprofit = request.user.nonprofit
    project.name = obj['name']
    project.slug = create_project_slug(project.name)
    project.details = obj['details']
    project.description = obj['description']
    project.responsible = obj['responsible']
    project.phone = obj['phone']
    project.email = obj['email']
    project.save()

    skills = obj['skills']
    for s in skills:
      project.skills.add(Skill.objects.get(id=s))

    causes = obj['causes']
    for c in causes:
      project.causes.add(Cause.objects.get(id=c))

    if obj.get('work', None):
      work =  Work()
      work.project = project
      work.weekly_hours = obj['work'].get('weekly_hours', 0)
      work.can_be_done_remotely = obj['work'].get('can_be_done_remotely', False)
      work.save()

      availabilities = obj['work'].get('availabilities', None)
      if availabilities:
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

    has_work = False
    has_job = False
    try:
      project.work
      has_work = True
    except:
      pass
    try:
      project.job
      has_job = True
    except:
      pass

    if not has_job and not has_work:
      return Response({'detail': 'Needs to have project or work.'}, status.HTTP_400_BAD_REQUEST)

    # Doing not required fields
    try:
      obja = obj.get('address', None)
      if obja:
          address = Address()
          address.addressline = obja.get('addressline', None)
          address.addressline2 = obja.get('addressline2', None)
          address.addressnumber = obja.get('addressnumber', None)
          address.neighborhood = obja.get('neighborhood', None)
          address.zipcode = obja.get('zipcode', None)
          if obja.get('city', None) and obja['city'].get('id', None):
              address.city = City.objects.get(id=obja['city']['id'])
          address.save()
          project.address = address
          project.save()

      project.facebook_event = obj.get('facebook_event', None)

      project.image = request.FILES.get('image')

      roles = obj.get('roles', None)
      if roles:
          for r in roles:
            role = Role()
            role.name = r['name']
            role.prerequisites = r['prerequisites']
            role.details = r['details']
            role.vacancies = r['vacancies']
            role.save()
            project.roles.add(role)
    except Exception as e:
      error = "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
      print error

  except Exception as e:
    error = "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
    return Response({'detail': error}, status.HTTP_400_BAD_REQUEST)

  project.save()
  return Response({'detail': 'Project succesfully created.', 'slug': project.slug}, status.HTTP_201_CREATED)

@api_view(['PUT'])
def confirm_email(request, format=None):
  try:
    token = json.loads(request.DATA['token'])
  except:
    token = request.DATA['token']

  try:
    user = User.objects.get(token=token)
    user.is_email_verified = True
    user.save()
  except Exception as e:
    error = "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
    return Response({'detail': error}, status.HTTP_400_BAD_REQUEST)

  return Response(user.email, status.HTTP_200_OK)

@api_view(['PUT'])
def open_project(request, format=None):
  # Need a nonprofit user
  try:
    request.user.nonprofit
  except Exception as e:
    error = "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
    return Response({"User not authenticated. " + error}, status.HTTP_403_FORBIDDEN)

  try:
    project_id = json.loads(request.DATA['project'])
  except:
    project_id = request.DATA['project']

  try:
    project = Project.objects.get(id=project_id)
  except:
    return Response({"No project with id " + project_id}, status.HTTP_400_BAD_REQUEST)

  project.closed = False;
  project.save()
  return Response(project.closed, status.HTTP_200_OK)

@api_view(['PUT'])
def close_project(request, format=None):
  # Need a nonprofit user
  try:
    request.user.nonprofit
  except Exception as e:
    error = "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
    return Response({"User not authenticated. " + error}, status.HTTP_403_FORBIDDEN)

  try:
    project_id = json.loads(request.DATA['project'])
  except:
    project_id = request.DATA['project']

  try:
    project = Project.objects.get(id=project_id)
  except:
    return Response({"No project with id " + project_id}, status.HTTP_400_BAD_REQUEST)

  project.closed = True;
  project.save()
  return Response(project.closed, status.HTTP_200_OK)

@api_view(['PUT'])
def save_project(request, format=None):
  # Need a nonprofit user
  try:
    request.user.nonprofit
  except Exception as e:
    error = "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
    return Response({"User not authenticated. " + error}, status.HTTP_403_FORBIDDEN)

  try:
    obj = json.loads(request.DATA['project'])
  except:
    obj = request.DATA['project']

  project = Project.objects.get(id=obj['id'])

  try:
    if obj['name'] != project.name:
      slug = create_project_slug(obj['name'])
    else:
      slug = project.slug
    project.name = obj['name']
    # Renaming the image file if the slug has changed
    if slug != project.slug and project.image.name:
      try:
        c = boto.connect_s3()
        bucket = c.get_bucket('atadosapp')
        k = bucket.get_key(project.image.name)
        if k:
          name = "project/%s/%s.jpg" % (project.nonprofit.user.slug, obj['slug'])
          if name != project.image.name:
            k.copy('atadosapp', name)
            k.delete()
            project.image.name = name;
        else:
          return Response({'detail': 'Could not get boto key to change project image name on S3.'}, status.HTTP_400_BAD_REQUEST)
      except Exception as e:
        print e
        pass

    project.slug = slug
    project.details = obj['details']
    project.description = obj['description']
    project.facebook_event = obj.get('facebook_event', None)
    project.responsible = obj['responsible']
    project.phone = obj['phone']
    project.email = obj['email']

    obja = obj.get('address', None)
    if obja:
      if project.address:
        address = project.address
      else:
        address = Address()
      address.addressline = obja.get('addressline', '')
      address.addressline2 = obja.get('addressline2', '')
      address.addressnumber = obja.get('addressnumber', '')
      address.neighborhood = obja.get('neighborhood', '')
      address.zipcode = obja.get('zipcode', '')
      address.city = City.objects.get(id=obja.get('city', None))
      address.save()

    roles = obj.get('roles', [])

    # Remove the roles that were deleted
    for pr in project.roles.all():
      found = False

      for r in roles:
        if r.get('id', None) == pr.id:
          found = True

      if not found:
        project.roles.remove(pr)

    for r in roles:
      found = False
      for pr in project.roles.all():
        if r.get('id', None) == pr.id:
          found = True
      if found:
        role = Role.objects.get(id=r['id'])
      else:
        role = Role()
      role.name = r.get('name', '')
      role.prerequisites = r.get('prerequisites', '')
      role.details = r.get('details', '')
      role.vacancies = r.get('vacancies', 1)
      role.save()
      project.roles.add(role)

    # Removing all skills then adding new ones
    skills = obj.get('skills', [])
    for s in project.skills.all():
      project.skills.remove(s)

    for s in skills:
      project.skills.add(Skill.objects.get(id=s))

    # Removing all causes then adding new ones
    causes = obj.get('causes', None)
    for c in project.causes.all():
      project.causes.remove(c)

    for c in causes:
      project.causes.add(Cause.objects.get(id=c))

    if obj.get('work', None):
      try:
        work = project.work
      except:
        work = Work()
        work.project = project
      work.weekly_hours = obj['work'].get('weekly_hours', 0)
      work.can_be_done_remotely = obj['work'].get('can_be_done_remotely', None)
      work.save()

      if obj['work'].get('availabilities', None):
        for a in project.work.availabilities.all():
          project.work.availabilities.remove(a)

        availabilities = obj['work']['availabilities']

        for a in availabilities:
          availability = Availability()
          availability.weekday = a['weekday']
          availability.period = a['period']
          availability.save()
          work.availabilities.add(availability)
      else:
        project.work.availabilities = []

      work.save()
      try:
        project.job.delete()
        project.job = None
      except:
        pass

    elif obj.get('job', None):
      try:
        job = project.job
      except:
        job = Job()
        job.project = project
      job.start_date = datetime.utcfromtimestamp(obj['job']['start_date']/1000).replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
      job.end_date = datetime.utcfromtimestamp(obj['job']['end_date']/1000).replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
      job.save()
      try:
        project.work.delete()
        project.work = None
      except:
        pass

    project.save()

  except Exception as e:
    error = "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
    return Response({'detail': error}, status.HTTP_400_BAD_REQUEST)

  return Response(ProjectSerializer(project).data, status.HTTP_201_CREATED)


@api_view(['POST'])
def password_reset(request, format=None):
  try:
    email = request.DATA['email']
    user = User.objects.get(email=email)
    password = User.objects.make_random_password()
    user.set_password(password)
    user.save()

    # Sending password reset email
    plaintext = 'Sua nova senha: '
    plaintext += password
    plaintext += u'. Por favor entre na sua conta e mude para algo de sua preferência. Qualquer dúvida retorne o email. Abraços.'
    html = plaintext
    subject, from_email, to = 'Nova senha do Atados', 'contato@atados.com.br', email
    msg = EmailMultiAlternatives(subject, plaintext, from_email, [to])
    msg.attach_alternative(html, "text/html")
    msg.send()
    return Response({"Password was sent."}, status.HTTP_200_OK)
  except Exception as e:
    print "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
    return Response({e}, status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def change_password(request, format=None):
  try:
    email = request.DATA['email']
    user = User.objects.get(email=email)
    password = request.DATA['password']
    user.set_password(password)
    user.save()
    return Response({"Password set successfully."}, status.HTTP_200_OK)
  except:
    return Response({"There was a problem setting your password."}, status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def upload_volunteer_image(request, format=None):
  if request.user.is_authenticated():
    volunteer = Volunteer.objects.get(user=request.user)
    volunteer.image = request.FILES.get('file')
    volunteer.save()
    return Response({"file": volunteer.get_image_url()}, status.HTTP_200_OK)
  return Response({"Not logged in."}, status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def upload_project_image(request, format=None):
  if request.user.is_authenticated():
    project = Project.objects.get(id=request.QUERY_PARAMS.get('id'))
    project.image = request.FILES.get('file')
    project.save()
    return Response({"file": project.get_image_url()}, status.HTTP_200_OK)
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
def applies(request, format=None):
  applies = Apply.objects.values('id', 'date', 'project__name', 'volunteer__user__name', 'volunteer__user__email', 'volunteer__user__phone', 'project__nonprofit__name')
  return Response(applies, status.HTTP_200_OK)

@api_view(['GET'])
def numbers(request, format=None):
  numbers = {}
  numbers['projects'] = Project.objects.filter(closed=False, published=True).count()
  numbers['volunteers'] = Volunteer.objects.count()
  numbers['nonprofits'] = Nonprofit.objects.filter(published=True).count()
  return Response(numbers, status.HTTP_200_OK)

@cache_control(must_revalidate=True, max_age=1200)
@api_view(['GET'])
def startup(request, format=None):
  data = {}

  try:
    # Getting website number
    data['numbers'] = {}
    data['numbers']['projects'] = Project.objects.filter(closed=False, published=True).count()
    data['numbers']['volunteers'] = Volunteer.objects.count()
    data['numbers']['nonprofits'] = Nonprofit.objects.filter(published=True).count()

    # Getting active cities
    data['cities'] = CitySerializer(City.objects.filter(active=True).order_by('id'), many=True).data

    # Getting states
    data['states'] = StateSerializer(State.objects.all().order_by('id'), many=True).data

    # Getting causes
    data['causes'] = CauseSerializer(Cause.objects.all().order_by('id'), many=True).data

    # Getting skills
    data['skills'] = SkillSerializer(Skill.objects.all().order_by('id'), many=True).data

    return Response(data, status.HTTP_200_OK)
  except Exception as e:
    print "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
    return Response({"Something went wrong on the models lookup."}, status.HTTP_400_BAD_REQUEST)

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
    if not request.user.is_email_verified:
      return Response({"403": "Volunteer has not actived its account by email."}, status.HTTP_403_FORBIDDEN)

    volunteer = Volunteer.objects.get(user=request.user)

    try:
        project = Project.objects.get(id=request.DATA['project'])
    except Exception as e:
      error = "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
      return Response({"No project id. " + error}, status.HTTP_400_BAD_REQUEST)

    message = request.DATA.get('message', '')
    phone = request.DATA.get('phone', '')
    name = request.DATA.get('name', volunteer.user.name)

    if name:
      if volunteer.user.name != name:
        volunteer.user.name = name
        volunteer.user.save()

    if phone:
      if volunteer.user.phone != phone:
        volunteer.user.phone = phone
        volunteer.user.save()

    try:
      # If apply exists, then cancel it
      apply = Apply.objects.get(project=project, volunteer=volunteer)
      if not apply.canceled:
        apply.canceled = True
        try:
          apply.status = ApplyStatus.objects.get(id=3) # Desistente
        except:
          apply.status = ApplyStatus(name="Desistente", id=3) # Desistente
        apply.save()
        # TODO remove 4 week email from message queue if passed 30 days
        return Response({"Canceled"}, status.HTTP_200_OK)

      else:
        apply.canceled = False
        try:
          apply.status = ApplyStatus.objects.get(id=2) # Candidato
        except:
          apply.status = ApplyStatus(name="Candidato", id=2) # Candidato
        apply.save()

        try:
          # Schedule email to be sent 30 days after this Apply
          eta = datetime.now() + timedelta(days=30)
          send_email_to_volunteer_after_4_weeks_of_apply.apply_async(
            eta=eta,
            kwargs={'project_id': project.id, 'volunteer_email': volunteer.user.email})
        except:
          pass

        #if pontual, schedule email to be sent 3 days before
        try:
          eta = project.job.start_date - timedelta(days=3)
          send_email_to_volunteer_3_days_before_pontual.apply_async(
            eta=eta,
            kwargs={'project_id': project.id, 'volunteer_email': volunteer.user.email})
        except:
          pass

        return Response({"Applied"}, status.HTTP_200_OK)

    except: # new apply
      apply = Apply()
      apply.project = project
      apply.volunteer = volunteer
      try:
        apply.status = ApplyStatus.objects.get(id=2) # Candidato
      except:
        apply.status = ApplyStatus(name="Candidato", id=2) # Candidato
      apply.save()

      try:
        # Sending email to volunteer after user applied to project
        plaintext = get_template('email/volunteerAppliesToProject.txt')
        htmly     = get_template('email/volunteerAppliesToProject.html')
        d = Context({ 'project_name': project.name })
        subject, from_email, to = u'Confirmação do ato. Parabéns.', 'contato@atados.com.br', volunteer.user.email
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
      except:
        pass

      try:
        # Sending email to nonprofit after user applied to project
        plaintext = get_template('email/nonprofitGetsNotifiedAboutApply.txt')
        htmly     = get_template('email/nonprofitGetsNotifiedAboutApply.html')
        d = Context({ 'volunteer_name': volunteer.user.name, "volunteer_email": volunteer.user.email, "volunteer_phone": volunteer.user.phone, "volunteer_message": message, "project_name": project.name})
        email = project.email if project.email else project.nonprofit.user.email
        subject, from_email, to = u'Um voluntário se candidatou a seu ato!', 'contato@atados.com.br', email
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
      except:
        pass


      try:
        # Schedule email to be sent 30 days after this Apply
        eta = datetime.now() + timedelta(days=30)
        send_email_to_volunteer_after_4_weeks_of_apply.apply_async(
          eta=eta,
          kwargs={'project_id': project.id, 'volunteer_email': volunteer.user.email})
      except:
        pass

      #if pontual, schedule email to be sent 3 days before
      try:
        eta = project.job.start_date - timedelta(days=3)
        send_email_to_volunteer_3_days_before_pontual.apply_async(
          eta=eta,
          kwargs={'project_id': project.id, 'volunteer_email': volunteer.user.email})
      except:
        pass

      return Response({"Applied"}, status.HTTP_200_OK)

  return Response({"No user logged in."}, status.HTTP_403_FORBIDDEN)

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
    except Exception as e:
      print "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
      return Response({"Some error cloning the project."}, status.HTTP_400_BAD_REQUEST)
  return Response({"Some error cloning the project."}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def export_project_csv(request, project_slug, format=None):
  if request.user.is_authenticated():
    try:
      project = Project.objects.get(slug=project_slug)
      data = VolunteerResource().export(project.get_volunteers()).csv
      return Response({'volunteers': data}, status.HTTP_200_OK)
    except Exception as e:
      print "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
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

  def get_queryset(self):
    params = self.request.GET

    highlighted = params.get('highlighted') == 'true'
    if highlighted:
        return Project.objects.filter(highlighted=highlighted)

    query = params.get('query', None)
    cause = params.get('cause', None)
    skill = params.get('skill', None)
    city = params.get('city', None)
    nonprofit = params.get('nonprofit', None)

    if nonprofit:
      nonprofit = Nonprofit.objects.get(user__slug=nonprofit)
      queryset = Project.objects.filter(nonprofit=nonprofit)
    else:
        queryset = SearchQuerySet().models(Project)
    queryset = queryset.filter(causes=cause) if cause else queryset
    queryset = queryset.filter(skills=skill) if skill else queryset
    queryset = queryset.filter(city=city) if city else queryset
    queryset = queryset.filter(content=query) if query else queryset
    queryset = queryset.values_list('pk')
    results = [item for sublist in queryset for item in sublist]

    return Project.objects.filter(pk__in=results, deleted=False, closed=False, published=True).order_by('-highlighted')

class ProjectMapList(generics.ListAPIView):
  serializer_class = ProjectMapSerializer

  def get_queryset(self):
    return Project.objects.filter(deleted=False, closed=False, published=True)

class NonprofitList(generics.ListAPIView):
  serializer_class = NonprofitSearchSerializer
  permission_classes = [AllowAny]

  def get_queryset(self):
    params = self.request.GET

    highlighted = params.get('highlighted') == 'true'
    if highlighted:
        return Nonprofit.objects.filter(highlighted=highlighted)

    query = params.get('query', None)
    cause = params.get('cause', None)
    city = params.get('city', None)

    city = int(city) if city else None
    cause = int(cause) if cause else None

    queryset = SearchQuerySet().models(Nonprofit)
    queryset = queryset.filter(causes=cause) if cause else queryset
    queryset = queryset.filter(city=city) if city else queryset
    queryset = queryset.filter(content=query) if query else queryset
    queryset = queryset.values_list('pk')
    results = [item for sublist in queryset for item in sublist]

    return Nonprofit.objects.filter(pk__in=results, published=True, deleted=False).order_by('-highlighted')

class NonprofitMapList(generics.ListAPIView):
  serializer_class = NonprofitMapSerializer

  def get_queryset(self):
    return Nonprofit.objects.filter(deleted=False, published=True)

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

class JobViewSet(viewsets.ModelViewSet):
  queryset = Job.objects.all()
  serializer_class = JobSerializer

class WorkViewSet(viewsets.ModelViewSet):
  queryset = Work.objects.all()
  serializer_class = WorkSerializer

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
  queryset = Cause.objects.all().order_by('id')
  serializer_class = CauseSerializer
  permission_classes = [AllowAny]
  lookup_field = 'id'

class SkillViewSet(viewsets.ModelViewSet):
  queryset = Skill.objects.all().order_by('id')
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
