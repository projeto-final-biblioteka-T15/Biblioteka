from rest_framework import serializers
from books.models import Book
from users.models import User


class BookSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Book
        fields = ["id", "title", "published_date", "users"]
        read_only_fields = [
            "id",
        ]

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance: Book, validated_data: dict) -> Book:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
