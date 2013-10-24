from atados_core.models import Nonprofit, Volunteer, Project, Availability, Cause, Skill, State, City, Suburb, Address, Donation, Work, Material, Role, Apply, Recommendation
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('email', 'username', 'first_name', 'last_name')
    lookup_field = 'username'

class AvailabilitySerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model  = Availability
    fields = ('weekday', 'period')

class CauseSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Cause
    lookup_field = 'id'
    fields = ('url', 'name')

class SkillSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Skill
    lookup_field = 'id'
    fields = ('url', 'name')

class StateSerializer(serializers.ModelSerializer):
  class Meta:
    model = State
    fields = ('id', 'name', 'code')

class CitySerializer(serializers.ModelSerializer):
  class Meta:
    model = City
    fields = ('id', 'name', 'state')

class SuburbSerializer(serializers.ModelSerializer):
  class Meta:
    model = Suburb
    fields = ('id', 'name', 'city')

class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = Address
    depth = 1
    fields = ('id', 'zipcode', 'addressline', 'addressnumber', 'neighborhood', 'state',
              'city', 'suburb')

class DonationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Donation
    fields = ('id', 'project', 'delivery')

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

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Project
    fields = ('name', 'nonprofit', 'causes', 'slug', 'details', 'description',
              'responsible', 'phone', 'email', 'published', 'closed')

class NonprofitSerializer(serializers.HyperlinkedModelSerializer):
  user = UserSerializer()
  causes = CauseSerializer()
  role = serializers.Field(source='get_role')
  image_url = serializers.CharField(source='get_image_url', required=False)
  cover_url = serializers.CharField(source='get_cover_url')

  class Meta:
    model = Nonprofit
    lookup_field = 'slug'
    depth = 2
    fields = ('user', 'slug', 'image_url', 'cover_url', 'name', 'causes', 'details', 'description', 
              'phone', 'facebook_page', 'google_page', 'twitter_handle', 'address', 'role')

class VolunteerSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  causes = serializers.HyperlinkedRelatedField(many=True, view_name='cause-detail', lookup_field='id')
  skills  = serializers.HyperlinkedRelatedField(many=True, view_name='skill-detail', lookup_field='id')
  username = serializers.Field(source='user.username')
  role = serializers.Field(source='get_role')
  image_url = serializers.CharField(source='get_image_url', required=False)

  class Meta:
    model = Volunteer
    lookup_field = 'username'
    fields = ('user', 'username', 'image_url', 'causes', 'skills', 'phone', 'address', 'role')
