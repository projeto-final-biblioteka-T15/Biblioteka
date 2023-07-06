from rest_framework import serializers
from .models import Review
from books.models import Book
from users.models import User
from django.shortcuts import get_object_or_404
from copies.models import Copies


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "book", "user", "review_text", "rating", "created_at"]
        read_only_fields = ["id", "created_at", "user", "book"]

    def create(self, validated_data):
        copy_id = self.context["view"].kwargs["pk"]
        copy = get_object_or_404(Copies, pk=copy_id)

        book = copy.book
        user = self.context["request"].user

        return Review.objects.create(book=book, user=user, **validated_data)
