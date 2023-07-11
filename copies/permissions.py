from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Copies
from .views import BookFollower


class IsLibraryStaffOrBookFollower(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_type == 'library_staff':
            return True
        elif request.method in ['GET'] and request.user.is_authenticated:
            copy_id = view.kwargs.get('pk')
            copy = get_object_or_404(Copies, pk=copy_id)
            book_follower = BookFollower.objects.filter(user=request.user, book=copy.book).exists()
            return book_follower
        return False
