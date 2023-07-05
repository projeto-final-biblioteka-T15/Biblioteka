from rest_framework import permissions

class IsLibraryStaffOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.user_type == 'library_staff'
