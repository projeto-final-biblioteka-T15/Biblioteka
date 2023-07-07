from django.db import models
from books.models import Book
from users.models import User
from loans.models import Loan
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    review_text = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateField(auto_now_add=True)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def create_review(cls, book, user, review_text, rating):
        loaned_and_returned = Loan.objects.filter(
            Q(copy_book=book) & Q(user=user) & Q(returned=True)
        ).exists()

        if not loaned_and_returned:
            raise Exception(
                {"message": "You can't review this book before borrowing it."}
            )

        review = cls.objects.create(
            book=book, user=user, review_text=review_text, rating=rating
        )
        return review
