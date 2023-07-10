from rest_framework import serializers
from .models import Review
from django.shortcuts import get_object_or_404
from copies.models import Copies


class ReviewSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format="%Y-%m-%d", read_only=True)
    updated_at = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "book", "user", "review_text", "rating", "created_at", "updated_at"]
        read_only_fields = ["id", "book", "user", "created_at", "updated_at"]

    def create(self, validated_data):
        copy_id = self.context["view"].kwargs["pk"]
        copy = get_object_or_404(Copies, pk=copy_id)

        book = copy.book
        user = self.context["request"].user

        return Review.create_review(
            book=book,
            user=user,
            review_text=validated_data.get("review_text"),
            rating=validated_data.get("rating"),
        )
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context["request"].method == "PATCH":
            representation["updated_at"] = instance.updated_at
        else:
            representation.pop("updated_at", None)
        return representation
