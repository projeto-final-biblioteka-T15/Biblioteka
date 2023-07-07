from django.db import models
from users.models import User


class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    description = models.TextField()
    published_date = models.DateField(auto_now_add=True)

    book_created_by = models.ManyToManyField(User, through="BookOwner")


class BookOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
