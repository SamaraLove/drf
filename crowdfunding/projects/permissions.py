from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj,'owner'):
            return obj.owner == request.user
        if hasattr(obj,'supporter'):
            return obj.supporter == request.user

class isSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser