from tkinter import CASCADE
from django.db import models


class Book(models.Model):
    class Meta:
        ordering = ["id"]

    title = models.CharField(max_length=255, unique=True)
    published_date = models.DateField()

    owners = models.ForeignKey("users.User", on_delete=CASCADE, related_name="books")
    # users = models.ManyToManyField(Users)
