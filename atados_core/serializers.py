from atados_core.models import Nonprofit, Volunteer, Project
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'first_name', 'last_name', 'email')

#class PasswordSerializer(serializers.Serializer):
#  class Meta:
#    model = password
#    # probably need to decrypt password that clients passes
#
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
