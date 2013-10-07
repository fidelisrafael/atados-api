from atados_core.models import (Nonprofit, Volunteer, Project,
                                Donation, Work, Role, Apply, Recommendation)
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'first_name', 'last_name', 'email')

class VolunteerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Volunteer
    fields = ('id', 'user', 'causes', 'skills', 'address', 'phone')

class NonprofitSerializer(serializers.ModelSerializer):
  class Meta:
    model = Nonprofit
    fields = ('id', 'user', 'causes', 'slug', 'details', 'description',
              'phone', 'address', 'published', 'deleted', 'deleted_date')

class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Project
    fields = ('id', 'name', 'nonprofit', 'causes', 'slug', 'details', 'description',
              'responsible', 'phone', 'email', 'published', 'closed', 'deleted', 'deleted_date')

class DonationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Donation
    fields = ('id', 'project', 'delivery', 'collection_by_nonprofit')

class WorkSerializer(serializers.ModelSerializer):
  class Meta:
    model = Work
    fields = ('id', 'project', 'address', 'availabilities', 'skills', 'weekly_hours', 'can_be_done_remotely')

class RoleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Role
    fields = {'id', 'work', 'name', 'prerequisites', 'vacancies'}

class ApplySerializer(serializers.ModelSerializer):
  class Meta:
    model = Apply
    fields = {'id', 'volunteer', 'project', 'date'}

class RecommendationSerializer(serializers.ModelSerializer):
  class Meat:
    model = Recommendation
    fields = {'project', 'sort', 'state', 'city'}
