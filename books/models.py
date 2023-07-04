from django.db import models
from users.models import User


class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    published_date = models.DateField()

    book_created_by = models.ManyToManyField(User, through="BookOwner")
    # users = models.ManyToManyField(User, related_name="books")


class BookOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
