from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Estudante'),
        ('library_staff', 'Colaborador da biblioteca'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=127)