from atados_core.models import (Nonprofit, Volunteer, Project, Availability, Cause,
  Skill, State, City, Address, Work, Role,
  Apply, Recommendation, Job, User)
from rest_framework import serializers

class StateSerializer(serializers.ModelSerializer):
  class Meta:
    model = State
    fields = ('id', 'name', 'code')

class CitySerializer(serializers.ModelSerializer):
  state = StateSerializer(read_only=True)

  class Meta:
    model = City
    fields = ('id', 'name', 'state', 'active')

class AddressSerializer(serializers.ModelSerializer):
  city_state = serializers.CharField(source="get_city_state", required=False)

  class Meta:
    model = Address

    fields = ('id', 'zipcode', 'addressline', 'addressnumber', 'neighborhood', 'city', 'latitude', 'longitude', 'city_state')

class UserSerializer(serializers.ModelSerializer):
  address = AddressSerializer(source="get_address")

  class Meta:
    model = User
    lookup_field = 'slug'
    depth = 1
    fields = ('email', 'slug', 'name', 'phone', 'address', 'is_staff')

class EditableUserSerializer(serializers.ModelSerializer):
  address = AddressSerializer()

  class Meta:
    model = User
    lookup_field = 'slug'
    depth = 1
    fields = ('email', 'slug', 'name', 'phone', 'address', 'is_staff')

class VolunteerUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    lookup_field = 'slug'
    depth = 1
    fields = ('email', 'slug', 'name', 'phone', 'address', 'is_staff')

class AvailabilitySerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model  = Availability
    fields = ('weekday', 'period')

class CauseSerializer(serializers.ModelSerializer):
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
    fields = ('id', 'availabilities', 'weekly_hours', 'can_be_done_remotely')

class RoleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Role
    fields = ('id', 'name', 'prerequisites', 'vacancies', 'details')

class JobSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Job
    depth = 1
    fields = ('id', 'start_date', 'end_date')

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

class VolunteerProjectSerializer(serializers.ModelSerializer):
  name = serializers.CharField(source="user.name")
  email = serializers.CharField(source="get_email")
  phone = serializers.CharField(source="get_phone")
  slug = serializers.CharField(source="user.slug")

  class Meta:
    model = Volunteer
    lookup_field = 'slug'
    fields = ('name', 'email', 'phone', 'slug')

class VolunteerSlimSerializer(serializers.ModelSerializer):
  slug = serializers.CharField(source="user.slug")
  image_url = serializers.CharField(source="get_image_url")

  class Meta:
    model = Volunteer
    lookup_field = 'slug'
    fields = ('slug', 'image_url')

class NonprofitProjectSerializer(serializers.ModelSerializer):
  user = UserSerializer(required=False)
  slug = serializers.Field(source='user.slug')
  role = serializers.Field(source='get_type')
  image_url = serializers.CharField(source='get_image_url', required=False)
  cover_url = serializers.CharField(source='get_cover_url', required=False)
  name = serializers.CharField(source="name", required=False)
  causes = serializers.PrimaryKeyRelatedField(many=True)

  class Meta:
    model = Nonprofit
    lookup_field = 'slug'
    depth = 1
    fields = ('id', 'user', 'slug', 'image_url', 'cover_url', 'name', 'causes', 'details', 'description', 
              'website', 'facebook_page', 'google_page', 'twitter_handle', 'role', 'published')


class ProjectSerializer(serializers.ModelSerializer):
  causes = serializers.PrimaryKeyRelatedField(many=True)
  skills = serializers.PrimaryKeyRelatedField(many=True)
  job = JobSerializer(required=False)
  work = WorkSerializer(required=False)
  address = AddressSerializer(required=False)
  slug = serializers.CharField(source="slug", required=False)
  details = serializers.CharField(source="details", required=False)
  image_url = serializers.CharField(source='get_image_url', required=False)
  nonprofit = NonprofitProjectSerializer(required=False)
  nonprofit_image = serializers.CharField(source="nonprofit.get_image_url", required=False)
  nonprofit_city_state = serializers.CharField(source="nonprofit.user.address.get_city_state", required=False)
  name = serializers.CharField(source='name', required=False)
  roles = RoleSerializer(required=False)
  volunteers = VolunteerSlimSerializer(source='get_volunteers', required=False)
  volunteers_numbers = serializers.CharField(source='get_volunteers_numbers', required=False)

  class Meta:
    model = Project
    lookup_field = 'slug'
    depth = 1
    fields = ('id', 'causes', 'name', 'volunteers', 'slug', 'details', 'description', 'facebook_event',
              'responsible', 'address', 'phone', 'email', 'published', 'closed', 'deleted', 'volunteers_numbers',
              'work', 'job', 'image_url', 'skills', 'roles', 'nonprofit', 'nonprofit_image', 'nonprofit_city_state')

class ProjectMapSerializer(serializers.ModelSerializer):
  name = serializers.CharField(source='name', required=False)
  slug = serializers.CharField(source="slug", required=False)

  class Meta:
    model = Project
    lookup_field = 'slug'
    depth = 1
    fields = ('name', 'slug','address')

class ProjectSearchSerializer(serializers.ModelSerializer):
  name = serializers.CharField(source='name', required=False)
  slug = serializers.CharField(source="slug", required=False)
  image_url = serializers.CharField(source='get_image_url', required=False)
  nonprofit_image = serializers.CharField(source="nonprofit.get_image_url", required=False)
  nonprofit_slug = serializers.CharField(source="nonprofit.user.slug", required=False)
  nonprofit_name = serializers.CharField(source="nonprofit.name", required=False)
  city_state = serializers.CharField(source="address.get_city_state", required=False)
  causes = CauseSerializer(required=False)
  skills = SkillSerializer(required=False)
  work = WorkSerializer(required=False)
  job = JobSerializer(required=False)
  volunteers_numbers = serializers.CharField(source='get_volunteers_numbers', required=False)

  class Meta:
    model = Project
    lookup_field = 'slug'
    depth = 2
    fields = ('id', 'causes', 'name', 'slug', 'description', 'job', 'work',
              'image_url', 'skills', 'nonprofit_image', 'city_state',
              'nonprofit_slug', 'nonprofit_name', 'address', 'volunteers_numbers')

class ProjectVolunteerSerializer(serializers.ModelSerializer):
  name = serializers.CharField(source='name', required=False)
  slug = serializers.CharField(source="slug", required=False)
  image_url = serializers.CharField(source='get_image_url', required=False)
  nonprofit_image = serializers.CharField(source="nonprofit.get_image_url", required=False)
  nonprofit_slug = serializers.CharField(source="nonprofit.user.slug", required=False)
  nonprofit_name = serializers.CharField(source="nonprofit.name", required=False)
  city_state = serializers.CharField(source="address.get_city_state", required=False)
  causes = CauseSerializer(required=False)
  skills = SkillSerializer(required=False)
  work = WorkSerializer(required=False)
  job = JobSerializer(required=False)
  volunteers_numbers = serializers.CharField(source='get_volunteers_numbers', required=False)

  class Meta:
    model = Project
    lookup_field = 'slug'
    depth = 2
    fields = ('id', 'causes', 'name', 'slug', 'description', 'job', 'work',
              'image_url', 'skills', 'nonprofit_image', 'city_state',
              'nonprofit_slug', 'nonprofit_name', 'volunteers_numbers')

class NonprofitSerializer(serializers.ModelSerializer):
  user = EditableUserSerializer(required=False)
  slug = serializers.Field(source='user.slug')
  role = serializers.Field(source='get_type')
  image_url = serializers.CharField(source='get_image_url', required=False)
  cover_url = serializers.CharField(source='get_cover_url', required=False)
  volunteers = VolunteerSlimSerializer(source='get_volunteers', required=False)
  volunteers_numbers = serializers.CharField(source='get_volunteers_numbers', required=False)
  projects = ProjectSerializer(source='get_projects', required=False)
  name = serializers.CharField(source="name", required=False)
  causes = serializers.PrimaryKeyRelatedField(many=True)

  class Meta:
    model = Nonprofit
    lookup_field = 'slug'
    depth = 2
    fields = ('id', 'user', 'slug', 'image_url', 'cover_url', 'name', 'causes', 'details', 'description', 
              'website', 'facebook_page', 'google_page', 'twitter_handle', 'role', 'volunteers', 'projects', 'published')

class NonprofitMapSerializer(serializers.ModelSerializer):
  name = serializers.CharField(source='name', required=False)
  slug = serializers.Field(source='user.slug')
  address = AddressSerializer(source='user.address')

  class Meta:
    model = Project
    lookup_field = 'slug'
    fields = ('name', 'slug','address')

class NonprofitSearchSerializer(serializers.ModelSerializer):
  slug = serializers.Field(source='user.slug')
  address = AddressSerializer(source='user.address')
  city_state = serializers.CharField(source="user.address.get_city_state", required=False)
  role = serializers.Field(source='get_type')
  image_url = serializers.CharField(source='get_image_url', required=False)
  cover_url = serializers.CharField(source='get_cover_url', required=False)
  name = serializers.CharField(source="name", required=False)
  causes = CauseSerializer(required=False)
  volunteers_numbers = serializers.CharField(source='get_volunteers_numbers', required=False)

  class Meta:
    model = Nonprofit
    lookup_field = 'slug'
    fields = ('id', 'address', 'city_state', 'slug', 'image_url', 'cover_url', 'name', 'causes',
              'description', 'role', 'volunteers_numbers')

class NonprofitVolunteerSerializer(serializers.ModelSerializer):
  user = EditableUserSerializer(required=False)
  slug = serializers.Field(source='user.slug')
  image_url = serializers.CharField(source='get_image_url')
  cover_url = serializers.CharField(source='get_cover_url')
  name = serializers.CharField(source="name")
  causes = serializers.PrimaryKeyRelatedField(many=True)
  volunteers_numbers = serializers.CharField(source='get_volunteers_numbers')
  city_state = serializers.CharField(source="user.address.get_city_state", required=False)

  class Meta:
    model = Nonprofit
    lookup_field = 'slug'
    depth = 2
    fields = ('id', 'user', 'slug', 'image_url', 'cover_url', 'name', 'causes', 'description', 'volunteers_numbers', 'city_state')

class VolunteerSerializer(serializers.ModelSerializer):
  user = VolunteerUserSerializer(required=False)
  slug = serializers.Field(source='user.slug')
  role = serializers.Field(source='get_type')
  image_url = serializers.CharField(source='get_image_url', required=False)
  birthDate = serializers.DateField(source="birthDate", required=False)
  causes = serializers.PrimaryKeyRelatedField(many=True)
  skills = serializers.PrimaryKeyRelatedField(many=True)

  class Meta:
    model = Volunteer
    lookup_field = 'slug'
    depth = 1
    fields = ('user', 'slug', 'image_url', 'causes', 'skills', 'role', 'facebook_uid', 'birthDate')

class VolunteerPublicSerializer(serializers.ModelSerializer):
  slug = serializers.Field(source='user.slug')
  name = serializers.Field(source='user.name')
  role = serializers.Field(source='get_type')
  image_url = serializers.CharField(source='get_image_url', required=False)
  causes = serializers.PrimaryKeyRelatedField(many=True)
  skills = serializers.PrimaryKeyRelatedField(many=True)
  projects = ProjectVolunteerSerializer(source="get_projects")
  nonprofits = NonprofitVolunteerSerializer(source="get_nonprofits")

  class Meta:
    model = Volunteer
    lookup_field = 'slug'
    depth = 1
    fields = ('slug', 'name', 'role', 'image_url', 'causes', 'skills', 'projects', 'nonprofits')
