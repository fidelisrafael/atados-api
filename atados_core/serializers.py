from atados_core.models import Nonprofit, Volunteer, Project, Availability, Cause, Skill, State, City, Suburb, Address, Donation, Work, Material, Role, Apply, Recommendation
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ( 'email', 'username', 'first_name', 'last_name')

class VolunteerSerializer(serializers.HyperlinkedModelSerializer):
  user = UserSerializer(many=False)

  class Meta:
    model = Volunteer
    fields = ('user', 'causes', 'skills', 'address', 'phone')

class NonprofitSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Nonprofit
    fields = ('slug', 'causes', 'details', 'description',  'phone', 'address')

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Project
    fields = ('name', 'nonprofit', 'causes', 'slug', 'details', 'description',
              'responsible', 'phone', 'email', 'published', 'closed')

class AvailabilitySerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model  = Availability
    fields = ('weekday', 'period')

class CauseSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Cause
    fields = ('name')

class SkillSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Skill
    fields = ('name')

class StateSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = State
    fields = ('name', 'code')

class CitySerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = City
    fields = ('name', 'state')

class SuburbSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Suburb
    fields = ('name', 'city')

class AddressSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Address
    fields = ('zipcode', 'addressline', 'addressnumber', 'neighborhood', 'state',
              'city', 'suburb')

class DonationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Donation
    fields = ('project', 'delivery')

class WorkSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Donation
    fields = ('project', 'address', 'availabilities', 'skills', 'weekly_hours', 'can_be_done_remotely')

class MaterialSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Material
    fields = ('donation', 'name', 'quantity')

class RoleSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Role
    fields = ('work', 'name', 'prerequisited', 'vacancies')

class ApplySerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Apply
    fields = ('volunteer', 'project', 'date')

class RecommendationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Recommendation
    fields = ('project', 'sort', 'state', 'city')
