from atados_core.models import (Nonprofit, Volunteer, Project, Availability, Cause,
  Skill, State, City, Suburb, Address, Donation, Work, Material, Role,
  Apply, Recommendation, Job, User)
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
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
  state = StateSerializer()

  class Meta:
    model = City
    fields = ('id', 'name', 'state')

class SuburbSerializer(serializers.ModelSerializer):
  class Meta:
    model = Suburb
    fields = ('id', 'name', 'city')

class AddressSerializer(serializers.ModelSerializer):
  city = CitySerializer()
  class Meta:
    model = Address
    depth = 1
    fields = ('id', 'zipcode', 'addressline', 'addressnumber', 'neighborhood', 'state',
              'city', 'suburb')

class WorkSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Work
    depth = 1
    fields = ('address', 'availabilities', 'skills', 'weekly_hours', 'can_be_done_remotely')

class MaterialSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Material
    fields = ('donation', 'name', 'quantity')

class DonationSerializer(serializers.ModelSerializer):
  materials = MaterialSerializer(required=True)
  class Meta:
    model = Donation
    depth = 1
    fields = ('delivery', 'collection_by_nonprofit', 'materials')

class RoleSerializer(serializers.HyperlinkedModelSerializer):

  def __init__(self, *args, **kwargs):
    many = kwargs.pop('many', True)
    super(RoleSerializer, self).__init__(*args, **kwargs)

  class Meta:
    model = Role
    fields = ('url', 'name', 'prerequisites', 'vacancies')

class JobSerializer(serializers.HyperlinkedModelSerializer):
  roles = serializers.PrimaryKeyRelatedField(many=True, read_only=False)
  skills  = serializers.HyperlinkedRelatedField(many=True, view_name='skill-detail', lookup_field='id')
  address = AddressSerializer()

  class Meta:
    model = Job
    depth = 1
    fields = ('address', 'skills','roles', 'start_date', 'end_date')

class ApplySerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Apply
    fields = ('volunteer', 'project', 'date')

class RecommendationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Recommendation
    fields = ('project', 'sort', 'state', 'city')

class NonprofitSerializer(serializers.HyperlinkedModelSerializer):
  user = UserSerializer()
  causes = CauseSerializer()
  slug = serializers.Field(source='user.slug')
  role = serializers.Field(source='get_type')
  image_url = serializers.CharField(source='get_image_url', required=False)
  cover_url = serializers.CharField(source='get_cover_url')

  class Meta:
    model = Nonprofit
    lookup_field = 'slug'
    depth = 1
    fields = ('url', 'user', 'slug', 'image_url', 'cover_url', 'name', 'causes', 'details', 'description', 
              'facebook_page', 'google_page', 'twitter_handle', 'role')

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
  causes = serializers.HyperlinkedRelatedField(many=True, view_name='cause-detail', lookup_field='id')
  nonprofit = NonprofitSerializer()
  work = WorkSerializer(required=False)
  job = JobSerializer(required=False)
  donation = DonationSerializer(required=False)
  image_url = serializers.CharField(source='get_image_url', required=False)

  class Meta:
    model = Project
    lookup_field = 'slug'
    depth = 1
    fields = ('nonprofit', 'causes', 'name', 'slug', 'details', 'description', 'facebook_event',
              'responsible', 'phone', 'email', 'published', 'closed', 'deleted',
              'job', 'work', 'donation', 'image_url')

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
