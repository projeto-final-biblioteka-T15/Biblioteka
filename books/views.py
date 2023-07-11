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
        book_id = self.request.query_params.get('book_id', None)

        if author:
            queryset = queryset.filter(author__icontains=author)
        
        if title:
            queryset = queryset.filter(title__icontains=title)

        if book_id:  
            queryset = queryset.filter(id=book_id)

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
