from django.db import models
from books.models import Book

class Copies(models.Model):
    total = models.PositiveIntegerField(default=0)
    available = models.PositiveIntegerField(default=0)

    book = models.ForeignKey(Book, related_name="copies", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("book",)
