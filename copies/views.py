from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Copies
from loans.models import Loan
from .serializers import CopiesSerializer, BookFollower
from .permissions import IsLibraryStaffOrAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from books.permissions import IsLibraryStaff
from .serializers import BookFollowerSerializer



class CopyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLibraryStaffOrAuthenticated | IsAuthenticatedOrReadOnly]

    queryset = Copies.objects.all()
    serializer_class = CopiesSerializer


class CopyDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLibraryStaff]

    queryset = Copies.objects.all()
    serializer_class = CopiesSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        allowed_fields = set(["total", "available"])
        updated_fields = set(request.data.keys())
        if not updated_fields.issubset(allowed_fields):
            raise ValidationError(
                "Apenas os campos 'total' e 'available' podem ser alterados."
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        loan = Loan.objects.filter(copy=instance, returned=False).first()
        if loan:
            instance.check_user_blocked(loan.user)

        return Response(serializer.data)


class BookFollowView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = BookFollower.objects.all()
    serializer_class = BookFollowerSerializer

    lookup_field = "pk"

    def create(self, request, *args, **kwargs):
        user = request.user
        copy_id = kwargs["pk"]
        copy = get_object_or_404(Copies, pk=copy_id)

        book = copy.book

        book_follower, created = BookFollower.objects.get_or_create(
            user=user, book=book
        )

        if created:
            return Response({"message": "Você agora está seguindo este livro."})
        else:
            return Response({"message": "Você já está seguindo este livro."})
