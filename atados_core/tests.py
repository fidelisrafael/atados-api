from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from atados_core.models import (Availability, Cause, Skill, State, City, User, Volunteer,
                                Comment, Project, Nonprofit, Address, Apply, ApplyStatus, Job)
from atados_core import views

import pytz
from datetime import datetime

# Models
class AvailabilityTest(TestCase):

  def create_availability(self, weekday=1, period=2):
    return Availability.objects.create(weekday=weekday, period=period)

  def test_availability_creation(self):
    """
    Tests Availability.
    """
    a = self.create_availability()
    self.assertTrue(isinstance(a, Availability))
    self.assertEqual(a.__unicode__(), "Segunda -  Noite")

class CauseTest(TestCase):

  cause = "Idosos"
  
  def create_cause(self, name=cause):
    return Cause.objects.create(name=name)

  def test_cause_creation(self):
    """
    Tests Cause.
    """
    c = self.create_cause()
    self.assertTrue(isinstance(c, Cause))
    self.assertEqual(c.__unicode__(), self.cause)

class SkillTest(TestCase):

  skill = "Direito"

  def create_skill(self, name=skill):
    return Skill.objects.create(name=name)

  def test_skill_creation(self):
    """
    Tests Skill.
    """
    s = self.create_skill()
    self.assertTrue(isinstance(s, Skill))
    self.assertEqual(s.__unicode__(), self.skill)

class StateTest(TestCase):

  def create_state(self, name="Rio de Janeiro", code="RJ"):
    return State(name=name, code=code)

  def test_state_creation(self):
    """
    Tests State.
    """
    s = self.create_state()
    self.assertTrue(isinstance(s, State))
    self.assertEqual(s.__unicode__(), "Rio de Janeiro")

def datesAreEqual(d1, d2):
  return d1.year == d2.year and d1.month == d2.month and d1.day == d2.day \
         and d1.hour == d2.hour and d1.minute == d2.minute

class ProjectCreateTest(APITestCase):
  fixtures = ['causes_skills.json']

  def create_project(self, nonprofit, name):
    project = Project(nonprofit=nonprofit, name=name)
    project.save()
    return project

  def test_project_date_creation(self):
    """
    Tests Project date creation.
    """
    u = User()
    u.save()
    n = Nonprofit(user=u, name="Nonprofit 1")
    n.save()
    p = self.create_project(n, "Project 1")
    now = datetime.utcnow().replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
    self.assertTrue(isinstance(p, Project))
    self.assertEqual(p.__unicode__(), "Project 1 - Nonprofit 1")
    self.assertTrue(datesAreEqual(p.created_date, now))
    self.assertTrue(datesAreEqual(p.modified_date, now))

  def test_project_date_editing(self):
    """
    Tests Project date editing.
    """
    u = User()
    u.save()
    n = Nonprofit(user=u, name="Nonprofit 1")
    n.save()
    p = self.create_project(n, "Project 1")
    self.assertEqual(p.__unicode__(), "Project 1 - Nonprofit 1")
    p.name = "Project 2"
    p.save()
    now = datetime.utcnow().replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
    self.assertTrue(datesAreEqual(p.modified_date, now))
    self.assertEqual(p.__unicode__(), "Project 2 - Nonprofit 1")

  def test_create_project_view_bad_request(self):
    """
    Project with bad data being sent.
    """
    factory = APIRequestFactory()
    request = factory.post("/create/project/", {"project": ""})
    u = User()
    u.save()
    n = Nonprofit(user=u)
    n.save()
    force_authenticate(request, user=u)
    response = views.create_project(request)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_project_view_not_authenticated(self):
    """
    Project with no authenticated user.
    """
    factory = APIRequestFactory()
    request = factory.post("/create/project/", {"project": ""})
    response = views.create_project(request)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_create_project_view_not_nonprofit_authenticated(self):
    """
    Project with user that is not nonprofit.
    """
    factory = APIRequestFactory()
    request = factory.post("/create/project/", {"project": ""})
    u = User()
    u.save()
    force_authenticate(request, user=u)
    response = views.create_project(request)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_create_project_view_with_only_required_fields_but_no_work_or_job(self):
    """
    Project with only required fields but no work or job.
    """
    factory = APIRequestFactory()
    project = {
      'name': "Name",
      'details': 'This needs to be big',
      'description': 'This needs to be big',
      'responsible': 'Marjor',
      'phone': '123123',
      'email': 'marjori@atados.com.br',
      'skills': [1],
      'causes': [2]
    }
    request = factory.post("/create/project/", {'project': project})
    u = User()
    u.save()
    n = Nonprofit(user=u)
    n.save()
    force_authenticate(request, user=u)
    response = views.create_project(request)
    self.assertEqual(response.data, {'detail': 'Needs to have project or work.'})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_project_view_with_only_required_fields_work(self):
    """
    Project work with only required fields and no availabilites.
    """
    factory = APIRequestFactory()
    project = {
      'name': "Name",
      'details': 'This needs to be big',
      'description': 'This needs to be big',
      'responsible': 'Marjor',
      'phone': '123123',
      'email': 'marjori@atados.com.br',
      'skills': [1],
      'causes': [2],
      'work': {
        'weekly_hours': 1,
        'can_be_done_remotely': True
      }
    }
    request = factory.post("/create/project/", {'project': project})
    u = User()
    u.save()
    n = Nonprofit(user=u)
    n.save()
    force_authenticate(request, user=u)
    response = views.create_project(request)
    self.assertEqual(response.data, {'detail': 'Project succesfully created.'})
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_create_project_view_with_only_required_fields_job(self):
    """
    Project job with only required fields and no availabilites.
    """
    factory = APIRequestFactory()
    project = {
      'name': "Name",
      'details': 'This needs to be big',
      'description': 'This needs to be big',
      'responsible': 'Marjor',
      'phone': '123123',
      'email': 'marjori@atados.com.br',
      'skills': [1],
      'causes': [2],
      'job': {
        'start_date': 20140416,
        'end_date': 20140417
      }
    }
    request = factory.post("/create/project/", {'project': project})
    u = User()
    u.save()
    n = Nonprofit(user=u)
    n.save()
    force_authenticate(request, user=u)
    response = views.create_project(request)
    self.assertEqual(response.data, {'detail': 'Project succesfully created.'})
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_create_two_project_same_slug(self):
    """
    Creating two projects with same name to see if different slugs are created..
    """
    factory = APIRequestFactory()
    project = {
      'name': "Name",
      'details': 'This needs to be big',
      'description': 'This needs to be big',
      'responsible': 'Marjor',
      'phone': '123123',
      'email': 'marjori@atados.com.br',
      'skills': [1],
      'causes': [2],
      'job': {
        'start_date': 20140416,
        'end_date': 20140417
      }
    }
    u = User()
    u.save()
    n = Nonprofit(user=u)
    n.save()
    request = factory.post("/create/project/", {'project': project})
    force_authenticate(request, user=u)
    response = views.create_project(request)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    request = factory.post("/create/project/", {'project': project})
    force_authenticate(request, user=u)
    response = views.create_project(request)
    self.assertEqual(response.data, {'detail': 'Project succesfully created.'})
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ProjectEditTest(APITestCase):
  fixtures = ['causes_skills.json']

  def test_edit_project_view_with_only_required_fields_job(self):
    """
    Project edit job with only required fields and no availabilites.
    """
    factory = APIRequestFactory()
    project = {
      'name': "Name",
      'details': 'This needs to be big',
      'description': 'This needs to be big',
      'responsible': 'Marjori',
      'phone': '123123',
      'email': 'marjori@atados.com.br',
      'skills': [1],
      'causes': [2],
      'job': {
        'start_date': 20140416,
        'end_date': 20140417
      },
      'nonprofit': 1
    }
    u = User()
    u.save()
    n = Nonprofit(user=u)
    n.save()
    p = Project(nonprofit=n, name=project['name'], slug="name", details=project['details'])
    p.save()
    project['id'] = p.id
    request = factory.put("/save/project/", {'project': project})
    force_authenticate(request, user=u)
    response = views.save_project(request)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CommentTest(TestCase):

  def create_comment(self, project, user, comment):
    return Comment(project=project, user=user, comment=comment)

  def test_comment_creation(self):
    """
    Tests Comment creation.
    """
    u1 = User(email="test", slug="user1") 
    u1.save()
    n = Nonprofit(user=u1)
    n.save()
    p = Project(name="Project 1", nonprofit=n)
    p.save()
    u = User(email="email@gmail.com", slug="email")
    u.save()
    c = self.create_comment(p, u, "Comment nro 1")
    c.save()
    now = datetime.utcnow().replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
    self.assertTrue(isinstance(c, Comment))
    self.assertEqual(c.__unicode__(), "(Project 1) email@gmail.com: Comment nro 1")
    self.assertTrue(datesAreEqual(c.created_date, now))

  def test_comment_deletion(self):
    """
    Tests Comment deletion.
    """
    u1 = User(email="test", slug="user1") 
    u1.save()
    n = Nonprofit(user=u1)
    n.save()
    p = Project(name="Project 1", nonprofit=n)
    p.save()
    u = User(email="email@gmail.com", slug="email")
    u.save()
    c = self.create_comment(p, u, "Comment nro 1")
    c.save()
    c.delete()
    self.assertTrue(c.deleted)
    self.assertTrue(c.deleted_date)

class ProjectTest(APITestCase):
  fixtures = ['causes_skills.json']

  def create_project(self, nonprofit, name):
    project = Project(nonprofit=nonprofit, name=name)
    project.save()
    return project

  def test_open_project(self):
    """
    Tests opening project that is closed.
    """
    u = User()
    u.save()
    n = Nonprofit(user=u, name="Nonprofit 1")
    n.save()
    p = self.create_project(n, "Project 1")
    p.closed = True;
    factory = APIRequestFactory()
    request = factory.put("/open/project/", {'project': p.id})
    force_authenticate(request, user=u)
    response = views.open_project(request)
    self.assertEqual(response.data, False)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_close_project(self):
    """
    Tests closing project that is open.
    """
    u = User()
    u.save()
    n = Nonprofit(user=u, name="Nonprofit 1")
    n.save()
    p = self.create_project(n, "Project 1")
    p.closed = False;
    factory = APIRequestFactory()
    request = factory.put("/close/project/", {'project': p.id})
    force_authenticate(request, user=u)
    response = views.close_project(request)
    self.assertEqual(response.data, True)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

class CityTest(TestCase):

  def create_city(self, name="Rio de Janeiro"):
    state = State(name="Rio de Janeiro", code="RJ")
    return City(name=name, state=state)

  def test_city_creation(self):
    """
    Tests City.
    """
    c = self.create_city()
    self.assertTrue(isinstance(c, City))
    self.assertEqual(c.__unicode__(), "Rio de Janeiro, RJ")

class AddressTest(TestCase):

  def create_address(self, zipcode="05432-001", addressline="Rua Hello World", addressnumber="123", addressline2="apt 1101",
                     neighborhood="Copacabana"):
    state = State(name="Rio de Janeiro", code="RJ")
    city = City(name="Rio de Janeiro", state=state)
    return Address.objects.create(zipcode=zipcode, addressline=addressline, addressnumber=addressnumber, addressline2=addressline2, neighborhood=neighborhood, city=city)

  def test_address_creation(self):
    """
    Tests Address.
    """
    a = self.create_address()
    self.assertTrue(isinstance(a, Address))
    self.assertEqual(a.__unicode__(),
                     "Rua Hello World, 123, apt 1101, Copacabana - Rio de Janeiro, RJ")

  def test_address_lat_long(self):
    """
    Tests Address if no latitude and longitude
    """
    a = Address()
    a.city = City(id=0, name="trabalho a distancia", state=State(name="blah", code="BL"))
    self.assertEqual(a.latitude, 0.0)
    self.assertEqual(a.longitude, 0.0)
    a = self.create_address()
    self.assertTrue(a.latitude != 0.0)
    self.assertTrue(a.longitude != 0.0)

class VolunteerTest(APITestCase):

  email = "test@test.com"
  slug = "test"
  name="Test"
  password = "hello world"

  def test_volunteer_creation(self):
    """
    Test Volunteer Model.
    """
    u = User(email=self.email, slug=self.slug, name=self.name)
    v = Volunteer.create(u)
    self.assertTrue(isinstance(v, Volunteer))
    self.assertEqual(v.__unicode__(), self.name)
    self.assertEqual(v.get_type(), "VOLUNTEER");
    self.assertEqual(v.image_name("teste.jpg"), "volunteer/" + self.slug + "/" + self.slug + ".jpg")


  def test_create_volunteer_view(self):
    """
    Ensure we can create a new volunteer.
    """
    factory = APIRequestFactory()
    request = factory.post("/create/volunteer/", {"slug": self.slug, "email": self.email, "password": self.password})
    response = views.create_volunteer(request)
    self.assertEqual(response.data, {'detail': 'Volunteer succesfully created.'})
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    user = User.objects.get(email=self.email)
    volunteer = user.volunteer
    self.assertEqual(volunteer.user.email, user.email)

class ApplyTest(APITestCase):

  def test_apply_creation(self):
    """
    Tests Apply.
    """
    u = User(name="Voluntario", slug="voluntario")
    u.save()
    v = Volunteer(user=u)
    v.save()
    p = Project(name="Project")
    a = Apply(status=ApplyStatus(), volunteer=v, project=p)
    self.assertTrue(isinstance(a, Apply))
    self.assertEqual(a.__unicode__(), "[False] Voluntario - Project")

  def create_project(self):
      u = User(email="project_user@gmail.com", name="what", slug="hahah")
      u.save()
      n = Nonprofit(user=u, name="hahah")
      n.save()
      from random import randint
      random = randint(1,100)
      project = Project(nonprofit=n, name='name' + str(random))
      project.nonprofit = n
      project.save()
      project.job = Job(start_date=datetime.now().replace(tzinfo=pytz.timezone("America/Sao_Paulo")), end_date=datetime.now().replace(tzinfo=pytz.timezone("America/Sao_Paulo")))
      project.job.save()
      return project

  def test_apply_volunteer_to_project_view(self):
    """
    Ensure we can apply a volunteer to a project.
    """
    a = ApplyStatus(name="Candidato", id=2)
    a.save()
    u = User(email="test@gmail.com", name="test", slug="test")
    u.is_email_verified = True
    u.save()
    volunteer = Volunteer(user=u)
    volunteer.save()
    project = self.create_project()
    factory = APIRequestFactory()
    request = factory.post("/apply_volunteer_to_project/", {"project": project.id, 'name': 'new name', 'phone': '3444-3434'})
    force_authenticate(request, user=volunteer.user)
    response = views.apply_volunteer_to_project(request)
    self.assertEqual(response.data, {'Applied'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    u = User.objects.get(slug='test')
    self.assertEqual('new name', u.name)
    self.assertEqual('3444-3434', u.phone)

  def test_apply_volunteer_to_project_view_not_verified(self):
    """
    Apply a volunteer not verified to a project.
    """
    a = ApplyStatus(name="Candidato", id=2)
    a.save()
    u = User(email="test@gmail.com", name="test", slug="test")
    u.save()
    volunteer = Volunteer(user=u)
    volunteer.save()
    project = self.create_project()
    factory = APIRequestFactory()
    request = factory.post("/apply_volunteer_to_project/", {"project": project.id})
    force_authenticate(request, user=volunteer.user)
    response = views.apply_volunteer_to_project(request)
    self.assertEqual(response.data, {"403": "Volunteer has not actived its account by email."})
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_apply_volunteer_to_project_view_without_auth(self):
    """
    Apply no volunteer to a project.
    """
    a = ApplyStatus(name="Candidato", id=2)
    a.save()
    u = User(email="test@gmail.com", name="test", slug="test")
    u.save()
    volunteer = Volunteer(user=u)
    volunteer.save()
    project = self.create_project()
    factory = APIRequestFactory()
    request = factory.post("/apply_volunteer_to_project/", {"project": project.id})
    response = views.apply_volunteer_to_project(request)
    self.assertEqual(response.data, {"No user logged in."})
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_apply_volunteer_to_project_view_without_project(self):
    """
    Apply volunteer to project without project id.
    """
    u = User(email="test@gmail.com", name="test", slug="test")
    u.is_email_verified = True
    u.save()
    volunteer = Volunteer(user=u)
    volunteer.save()
    factory = APIRequestFactory()
    request = factory.post("/apply_volunteer_to_project/", {"project": ''})
    force_authenticate(request, user=volunteer.user)
    response = views.apply_volunteer_to_project(request)
    self.assertEqual(response.data, {"No project id. ERROR - 769 - invalid literal for int() with base 10: ''"})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_apply_volunteer_to_project_view_already_apply(self):
    """
    Unaply when apply already exists.
    """
    u = User(email="test@gmail.com", name="test", slug="test")
    u.is_email_verified = True
    u.save()
    volunteer = Volunteer(user=u)
    volunteer.save()
    project = self.create_project()
    factory = APIRequestFactory()
    request = factory.post("/apply_volunteer_to_project/", {"project": project.id})
    force_authenticate(request, user=volunteer.user)
    response = views.apply_volunteer_to_project(request)
    self.assertEqual(response.data, {'Applied'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    request = factory.post("/apply_volunteer_to_project/", {"project": project.id})
    force_authenticate(request, user=volunteer.user)
    response = views.apply_volunteer_to_project(request)
    self.assertEqual(response.data, {'Canceled'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_apply_volunteer_to_project_view_after_canceled(self):
    """
    Apply again after canceled.
    """
    u = User(email="test@gmail.com", name="test", slug="test")
    u.is_email_verified = True
    u.save()
    volunteer = Volunteer(user=u)
    volunteer.save()
    project = self.create_project()
    factory = APIRequestFactory()
    request = factory.post("/apply_volunteer_to_project/", {"project": project.id})
    force_authenticate(request, user=volunteer.user)
    response = views.apply_volunteer_to_project(request)
    self.assertEqual(response.data, {'Applied'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    request = factory.post("/apply_volunteer_to_project/", {"project": project.id})
    force_authenticate(request, user=volunteer.user)
    response = views.apply_volunteer_to_project(request)
    self.assertEqual(response.data, {'Canceled'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    request = factory.post("/apply_volunteer_to_project/", {"project": project.id})
    force_authenticate(request, user=volunteer.user)
    response = views.apply_volunteer_to_project(request)
    self.assertEqual(response.data, {'Applied'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)

