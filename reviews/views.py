from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Review
from .serializer import ReviewSerializer
from django.shortcuts import get_object_or_404
from loans.models import Loan
from rest_framework.response import Response


class CreateReviewView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    lookup_field = "pk"


class ListReviewView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
