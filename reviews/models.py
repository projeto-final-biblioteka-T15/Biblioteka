from django.db import models
from books.models import Book
from users.models import User
from loans.models import Loan
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers


class Review(models.Model):
    review_text = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def create_review(cls, book, user, review_text, rating):
        review_exists = cls.objects.filter(book=book, user=user).exists()
        if review_exists:
            raise serializers.ValidationError(
                {"message": "You can't review this book twice."}
            )

        loaned_and_returned = Loan.objects.filter(
            Q(copy__book=book) & Q(user=user) & Q(returned=True)
        ).exists()

        if not loaned_and_returned:
            raise serializers.ValidationError(
                {"message": "You can't review this book before borrowing it."}
            )

        review = cls.objects.create(
            book=book, user=user, review_text=review_text, rating=rating
        )
        return review
