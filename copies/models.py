from django.db import models
from books.models import Book


class Copies(models.Model):
    total = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)

    book = models.ForeignKey(Book, related_name="copies", on_delete=models.CASCADE)
