from rest_framework import serializers
from .models import Copies
from books.models import Book
from books.serializers import BookSerializer
from books.models import Book
from .models import BookFollower


class BookFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFollower
        fields = ["id", "user", "book"]


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


# para testar o envio de e-mail
class SendEmailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    message = serializers.CharField()
    recipient_list = serializers.ListField()
