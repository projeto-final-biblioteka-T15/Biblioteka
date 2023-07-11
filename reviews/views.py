from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Review
from .serializer import ReviewSerializer
from .permissions import IsReviewOwner
from django.shortcuts import get_object_or_404
from copies.models import Copies
from datetime import date


class CreateReviewView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        copy_id = self.kwargs["pk"]
        copy = get_object_or_404(Copies, pk=copy_id)
        request.data["book"] = copy.book.id

        return super().create(request, *args, **kwargs)


class ListReviewView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        copy_id = self.request.query_params.get('copy_id')
        
        if copy_id:
            copy = get_object_or_404(Copies, id=copy_id)
            queryset = queryset.filter(book=copy.book)
        
        return queryset


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsReviewOwner]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_update(self, serializer):
        serializer.save(updated_at=date.today())
