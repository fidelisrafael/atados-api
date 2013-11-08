from django.test import TestCase

from atados_core.models import Availability, Cause, Skill, State, City, Suburb, Address, Nonprofit

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
    return State.objects.create(name=name, code=code)

  def test_state_creation(self):
    """
    Tests State.
    """
    s = self.create_state()
    self.assertTrue(isinstance(s, State))
    self.assertEqual(s.__unicode__(), "Rio de Janeiro")

class CityTest(TestCase):

  def create_city(self, name="Rio de Janeiro"):
    state = State.objects.create(name="Rio de Janeiro", code="RJ")
    return City.objects.create(name=name, state=state)

  def test_city_creation(self):
    """
    Tests City.
    """
    c = self.create_city()
    self.assertTrue(isinstance(c, City))
    self.assertEqual(c.__unicode__(), "Rio de Janeiro, RJ")

class SuburbTest(TestCase):

  def create_suburb(self, name="Zona Norte"):
    state = State.objects.create(name="Rio de Janeiro", code="RJ")
    city = City.objects.create(name="Rio de Janeiro", state=state)
    return Suburb.objects.create(name=name, city=city)

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
    state = State.objects.create(name="Rio de Janeiro", code="RJ")
    city = City.objects.create(name="Rio de Janeiro", state=state)
    suburb = Suburb.objects.create(name="Zona Norte", city=city)
    return Address.objects.create(zipcode=zipcode, addressline=addressline, addressnumber=addressnumber, addressline2=addressline2, neighborhood=neighborhood, state=state, city=city, suburb=suburb)

  def test_address_creation(self):
    """
    Tests Address.
    """
    a = self.create_address()
    self.assertTrue(isinstance(a, Address))
    self.assertEqual(a.__unicode__(),
                     "Rua Hello World, 123, apt 1101 - Copacabana - Zona Norte - Rio de Janeiro, RJ")

#class NonprofitTest(TestCase):
#
#  def create_nonprofit(self,):
#    return Nonprofit.objects.create()
#
#  def test_nonprofit_creation(self):
#    """
#    Tests Nonprofit.
#    """
#    n = self.create_nonprofit()
#    self.assertTrue(isinstance(n, Nonprofit))
#    self.assertEqual(n.__unicode__(), "")
