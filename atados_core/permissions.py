from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
  """
  Custom permission to only allow Owner of an object to edit it.
  """
  def has_object_permission(self, request, view, obj):
    # Read permissions are allowed to any request,
    # so we'll always allow GET, HEAD or OPTIONS requests.
    if request.method in permissions.SAFE_METHODS:            
      return True
  
    # Write permissions are only allowed to the owner of the snippet
    return request.user.is_staff or obj.user == request.user

class IsNonprofit(permissions.BasePermission):
  """
  Custom permission for accessign volunteer data from the Nonprofit panel
  """
  def has_object_permission(self, request, view, obj):
    if request.user.is_authenticated():
      return True if request.user.is_staff or request.user.nonprofit else False

  def has_permission(self, request, view, obj=None):
    if request.user.is_authenticated():
      return True if request.user.is_staff or request.user.nonprofit else False
