from rest_framework import permissions

class IsLibraryStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'library_staff'

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.user_type == 'library_staff'
