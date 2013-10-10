from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from atados_core.models import Nonprofit, Volunteer, Project
from atados_core.serializers import UserSerializer, NonprofitSerializer, VolunteerSerializer, ProjectSerializer

# Views the API need to provide
#
# 1. For unauthenticated/public users to view
#   - View a list of all open Projects
#   - View a list of all approved Nonprofits
#   - View a list of all approved 
#
# 2. Authenticated Volunteer
#   - update his Volunteer Profile
#   - view all open Projects
#   - view all Projects he has under his profile
#   - view all Nonprofits he has associations with 
#
# 3. Authenticated Nonprofit
#   - update Nonprofit Profile
#     - open projects
#     - closed projects
#   - create a Project
#   - view all open projects by all nonprofits
#   - view all open projects still on going for the non

@api_view(['GET'])
def current_user(request, format=None):
  if request.user.is_authenticated():
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
  else:
    content = {'error': 'No user logged in.'}
    return Response(content, status.HTTP_400_BAD_REQUEST)

# ERROR User could already be logged in
# ERRRO wrong credentials
# SUCCESS log in user
@api_view(['GET'])
def login(request, format=None):
  if request.user.is_authenticated():
    return Response({"User already logged in"}, status.HTTP_404_NOT_FOUND)
  else:
    # TODO actually login the user
    if susccess:
      return Response({"User logged in."}, status.HTTP_HTTP_200_OK)
    else:
      return Response({"Wrong credentials, could not login"}, status.HTTP_404_NOT_FOUND)

# ERROR No user logged in 
# LOGOUT User and expiry session?
@api_view(['GET'])
def logout(request, format=None):
  if not request.user.is_authenticated():
    return Response({"User already logged out"}, status.HTTP_404_NOT_FOUND)
  else:
    # TODO actually log out the user
    return Response({"User logged out."}, status.HTTP_HTTP_200_OK)

# Class based view alternative
#class CurrentUserView(APIView):
#    def get(self, request):
#        serializer = UserSerializer(request.user)
#        return Response(serializer.data)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

#  @action(permission_classes=[IsAdminOrIsSelf])
#  def set_password(self, request, pk=None): # TODO should I change this to username instead of 
#    user = self.get_object()
#    serializer = PasswordSerializer(data=request.DATA)
#    if serializer.is_valid():
#      user.set_password(serializer.data['password'])
#      user.save()
#      return Response({'status': 'password set'})
#    else:
#      return Response(serializer.errors,
#                      status=status.HTTP_400_BAD_REQUEST)
#
class NonprofitViewSet(viewsets.ModelViewSet):
  queryset = Nonprofit.objects.all()
  serializer_class = NonprofitSerializer
  # permission_classes = [IsOwnerOrReadOnly]

class VolunteerViewSet(viewsets.ModelViewSet):
  queryset = Volunteer.objects.all()
  serializer_class = VolunteerSerializer
  # permission_classes = [IsOwnerOrReadOnly]

  def get_queryset(self):
    """
    This view should return a list of all the purchases for the currently authenticated user.
    """
    user = self.request.user
    if (user.is_authenticated()):
      return Volunteer.objects.filter(user=user)
    else:
      return Volunteer.objects.all()

class ProjectViewSet(viewsets.ModelViewSet):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer
  # permissions_classes = [IsOwnerOrReadOnly]
