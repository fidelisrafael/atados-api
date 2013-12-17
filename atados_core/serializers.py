from atados_core.models import (Nonprofit, Volunteer, Project, Availability, Cause,
  Skill, State, City, Address, Work, Role,
  Apply, Recommendation, Job, User)
from rest_framework import serializers

class StateSerializer(serializers.ModelSerializer):
  class Meta:
    model = State
    fields = ('id', 'name', 'code')

class CitySerializer(serializers.ModelSerializer):
  state = StateSerializer()

  class Meta:
    model = City
    fields = ('id', 'name', 'state', 'active')

class AddressSerializer(serializers.ModelSerializer):
  city = CitySerializer()

  class Meta:
    model = Address
    fields = ('id', 'zipcode', 'addressline', 'addressnumber', 'neighborhood', 'city', 'latitude', 'longitude')

class UserSerializer(serializers.ModelSerializer):
  address = AddressSerializer()

  class Meta:
    model = User
    lookup_field = 'slug'
    depth = 1
    fields = ('email', 'slug', 'first_name', 'last_name', 'phone', 'address')

class AvailabilitySerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model  = Availability
    fields = ('weekday', 'period')

class CauseSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Cause
    lookup_field = 'id'
    fields = ('id', 'name')

class SkillSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Skill
    lookup_field = 'id'
    fields = ('id', 'name')

class WorkSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Work
    depth = 1
    fields = ('availabilities', 'weekly_hours', 'can_be_done_remotely')

class RoleSerializer(serializers.HyperlinkedModelSerializer):

  def __init__(self, *args, **kwargs):
    many = kwargs.pop('many', True)
    super(RoleSerializer, self).__init__(*args, **kwargs)

  class Meta:
    model = Role
    fields = ('url', 'name', 'prerequisites', 'vacancies')

class JobSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Job
    depth = 1
    fields = ('start_date', 'end_date')

class ApplySerializer(serializers.HyperlinkedModelSerializer):
  volunteer = serializers.Field(source="volunteer.user.slug")
  project = serializers.Field(source="project.slug")

  class Meta:
    model = Apply
    depth = 1
    fields = ('volunteer', 'project', 'date', 'project', 'status', 'canceled')

class RecommendationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Recommendation
    fields = ('project', 'sort', 'state', 'city')

class ProjectSerializer(serializers.ModelSerializer):
  causes = CauseSerializer()
  work = WorkSerializer(required=False)
  job = JobSerializer(required=False)
  address = AddressSerializer()
  image_url = serializers.CharField(source='get_image_url', required=False)
  volunteers = serializers.IntegerField(source='get_volunteers', required=True)

  class Meta:
    model = Project
    lookup_field = 'slug'
    depth = 2
    fields = ('id', 'causes', 'name', 'slug', 'details', 'description', 'facebook_event',
              'responsible', 'address', 'phone', 'email', 'published', 'closed', 'deleted',
              'job', 'work', 'image_url', 'volunteers', 'skills', 'roles', 'nonprofit')

class NonprofitSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  slug = serializers.Field(source='user.slug')
  role = serializers.Field(source='get_type')
  image_url = serializers.CharField(source='get_image_url', required=False)
  cover_url = serializers.CharField(source='get_cover_url')
  volunteers = serializers.IntegerField(source='get_volunteers', required=True)
  projects = ProjectSerializer(source='get_projects')

  class Meta:
    model = Nonprofit
    lookup_field = 'slug'
    depth = 1
    fields = ('id', 'user', 'slug', 'image_url', 'cover_url', 'name', 'causes', 'details', 'description', 
              'website', 'facebook_page', 'google_page', 'twitter_handle', 'role', 'volunteers', 'projects')

class VolunteerProjectSerializer(serializers.ModelSerializer):
  name = serializers.CharField(source="get_full_name")
  email = serializers.CharField(source="get_email")
  phone = serializers.CharField(source="get_phone")
  apply = ApplySerializer(source="get_apply")

  class Meta:
    model = Volunteer
    lookup_field = 'slug'
    fields = ('name', 'email', 'phone', 'apply')

class VolunteerSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  causes = serializers.HyperlinkedRelatedField(many=True, view_name='cause-detail', lookup_field='id')
  skills  = serializers.HyperlinkedRelatedField(many=True, view_name='skill-detail', lookup_field='id')
  slug = serializers.Field(source='user.slug')
  role = serializers.Field(source='get_type')
  image_url = serializers.CharField(source='get_image_url', required=False)

  class Meta:
    model = Volunteer
    lookup_field = 'slug'
    fields = ('user', 'slug', 'image_url', 'causes', 'skills', 'role')
