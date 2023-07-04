from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import BookSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsLibraryStaff


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLibraryStaff]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLibraryStaff]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
