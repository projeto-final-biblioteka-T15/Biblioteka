from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsLibraryStaff
from django.db.models import Q


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLibraryStaff]

    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()

        author = self.request.query_params.get('author', None)
        title = self.request.query_params.get('title', None)

        if author:
            queryset = queryset.filter(
                Q(author__icontains=author)
            )
        
        if title:
            queryset = queryset.filter(
                Q(title__icontains=title)
            )

        return queryset


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLibraryStaff]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListLatest(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLibraryStaff]

    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.all().order_by("-published_date")
