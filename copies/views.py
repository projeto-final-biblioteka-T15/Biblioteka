from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Copies
from loans.models import Loan
from .serializers import CopiesSerializer, BookFollower
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from books.permissions import IsLibraryStaff
from .serializers import BookFollowerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class CopyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = CopiesSerializer

    def get_queryset(self):
        queryset = Copies.objects.all()

        author = self.request.query_params.get('author', None)
        title = self.request.query_params.get('title', None)
        copy_id = self.request.query_params.get('copy_id', None)

        if author:
            queryset = queryset.filter(book__author__icontains=author)

        if title:
            queryset = queryset.filter(book__title__icontains=title)

        if copy_id:  
            queryset = queryset.filter(id=copy_id)

        return queryset


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


class BookFollowView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]

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


class BookListFollowersView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = BookFollowerSerializer

    def get_queryset(self):
        user = self.request.user
        copy_id = self.request.query_params.get('copy_id')
        user_id = self.request.query_params.get('user_id')

        if user.is_staff and copy_id:
            queryset = BookFollower.objects.filter(book_id=copy_id)
        elif user.is_staff and user_id:
            queryset = BookFollower.objects.filter(user_id=user_id, book__book_created_by=user)
        elif user.is_staff:
            queryset = BookFollower.objects.all()
        else:
            queryset = BookFollower.objects.filter(user=user)

        return queryset


class BookUnfollowView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = BookFollower.objects.all()

    def destroy(self, request, *args, **kwargs):
        user = request.user
        copy_id = kwargs["pk"]
        copy = get_object_or_404(Copies, pk=copy_id)

        book = copy.book

        try:
            book_follower = BookFollower.objects.get(user=user, book=book)
            book_follower.delete()
            return Response({"message": "Você deixou de seguir este livro."})
        except BookFollower.DoesNotExist:
            return Response(
                {"message": "Você não está seguindo este livro."},
                status=status.HTTP_404_NOT_FOUND
            )
