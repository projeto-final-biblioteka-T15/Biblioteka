from rest_framework import serializers
from .models import Copy
from books.serializers import BookSerializer


class CopySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Copy
        fields = ("id", "available", "book")
        read_only_fields = ("id",)

    def create(self, validated_data):
        book_data = self.context.get("book")
        copy = Copy.objects.create(book=book_data, **validated_data)
        return copy

    def update(self, instance: Copy, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
