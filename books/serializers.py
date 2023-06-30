from rest_framework import serializers
from books.models import Book


class BooksSerializer(serializers.ModelSerializer):
    # owners = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), many=True)

    class Meta:
        model = Book
        fields = ["id", "title", "published_date", "owners_id"]
        read_only_fields = [
            "id",
        ]

    def create(self, validated_data):
        return Book.objects.create(**validated_data)
 