from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from atados_core.models import Availability, Cause, Skill, State, City, Suburb, Address, Nonprofit, User, Volunteer
from atados_core import views

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

class SKillTest(TestCase):

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

class SuburbTest(TestCase):

  def create_suburb(self, name="Zona Norte"):
    state = State(name="Rio de Janeiro", code="RJ")
    city = City(name="Rio de Janeiro", state=state)
    return Suburb(name=name, city=city)

  def test_suburb_creation(self):
    """
    Tests Suburb.
    """
    s = self.create_suburb()
    self.assertTrue(isinstance(s, Suburb))
    self.assertEqual(s.__unicode__(), "Zona Norte - Rio de Janeiro, RJ")
    
class AddressTest(TestCase):

  def create_address(self, zipcode="05432-001", addressline="Rua Hello World", addressnumber="123", addressline2="apt 1101",
                     neighborhood="Copacabana"):
    state = State(name="Rio de Janeiro", code="RJ")
    city = City(name="Rio de Janeiro", state=state)
    suburb = Suburb(name="Zona Norte", city=city)
    return Address.objects.create(zipcode=zipcode, addressline=addressline, addressnumber=addressnumber, addressline2=addressline2, neighborhood=neighborhood, state=state, city=city, suburb=suburb)

  def test_address_creation(self):
    """
    Tests Address.
    """
    a = self.create_address()
    self.assertTrue(isinstance(a, Address))
    self.assertEqual(a.__unicode__(),
                     "Rua Hello World, 123, apt 1101 - Copacabana - Zona Norte - Rio de Janeiro, RJ")

# Views
class VolunteerTests(APITestCase):

  email = "test@test.com"
  slug = "testtest"
  password = "hello world"

  def test_volunteer_creation(self):
    """
    Test Volunteer Model.
    """
    u = User(email=self.email, slug=self.slug)
    v = Volunteer.create(u)
    self.assertTrue(isinstance(v, Volunteer))
    self.assertEqual(v.__unicode__(), self.slug)
    self.assertEqual(v.get_type(), "VOLUNTEER");
    self.assertEqual(v.get_image_url(), "http://atadosapp.s3.amazonaws.com/volunteer/default.png")
    self.assertEqual(v.image_name("teste.jpg"), "volunteer/" + self.slug + "/" + self.slug + ".jpg")


  def test_create_volunteer_view(self):
    """
    Ensure we can create a new volunteer.
    """
    factory = APIRequestFactory()
    request = factory.post("/create/volunteer/", {"slug": self.slug, "email": self.email, "password": self.password})
    response = views.create_volunteer(request)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data, {'detail': 'Volunteer succesfully created.'})
    user = User.objects.get(email=self.email)
    volunteer = user.volunteer
    self.assertEqual(volunteer.user.email, user.email)
