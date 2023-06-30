from rest_framework import serializers
from books.models import Book


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "published_date", "user_id"]
        read_only_fiels = ["id", "user_id"]

    def create(self, validated_data):
        return Book.objects.create(**validated_data)
 