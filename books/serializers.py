from rest_framework import serializers
from books.models import Book, BookOwner


class BookSerializer(serializers.ModelSerializer):
    book_created_by = serializers.SerializerMethodField()    

    class Meta:
        model = Book
        fields = ["id", "title", "author", "description", "published_date", "book_created_by"]
        read_only_fields = ["id", "published_date", "book_created_by"]
    
    def get_book_created_by(self, obj):
        return [{"name": user.name} for user in obj.book_created_by.all()]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None

        book = Book.objects.create(**validated_data)
        if user:
            BookOwner.objects.create(book=book, user=user)

        return book
