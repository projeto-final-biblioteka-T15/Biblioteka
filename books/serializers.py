from rest_framework import serializers
from books.models import Book, BookOwner
from users.serializers import UserSerializer


class BookSerializer(serializers.ModelSerializer):
    book_created_by = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "published_date", "book_created_by"]
        read_only_fields = ["id", "book_created_by"]

    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        book_owner = BookOwner.objects.create(
            book=book, user=self.context.get("request").user
        )

        return book

    def update(self, instance: Book, validated_data: dict) -> Book:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
