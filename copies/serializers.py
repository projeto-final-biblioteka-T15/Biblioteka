from rest_framework import serializers
from .models import Copy
from books.serializers import BooksSerializer


class CopySerializer(serializers.ModelSerializer):
    book = BooksSerializer(read_only=True)

    class Meta:
        model = Copy
        fields = ("id", "available", "book_id")
        read_only_fields = ("id",)

    def create(self, validated_data):
        book = self.context["book"]
        validated_data["book"] = book
        return Copy.objects.create(**validated_data)

    def update(self, instance: Copy, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
