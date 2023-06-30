from django.shortcuts import render
from .models import Copy
from .serializers import CopySerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication


class CopyView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JWTAuthentication,)

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")
        return Copy.objects.filter(book_id=book_id)
