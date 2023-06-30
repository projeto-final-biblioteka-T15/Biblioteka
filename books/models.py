from django.db import models
from users.models import User


class Book(models.Model):
    class Meta:
        ordering = ["id"]

    title = models.CharField(max_length=255, unique=True)
    published_date = models.DateField()

    users = models.ManyToManyField(User, related_name="books")
