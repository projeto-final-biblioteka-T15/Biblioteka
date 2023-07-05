from rest_framework import serializers
from .models import Copies
from books.models import Book
from books.serializers import BookSerializer, BookOwner


class CopiesSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Copies
        fields = ["id", "book", "total", "available"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        book = BookSerializer(instance.book).data
        representation["book"] = book
        return representation

    def create(self, validated_data):
        book_id = validated_data.pop("book").id
        book = Book.objects.get(id=book_id)        

        copies = Copies.objects.create(book=book, **validated_data)

        return copies
