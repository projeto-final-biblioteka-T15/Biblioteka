from django.db import models
from django.utils import timezone


class Loan(models.Model):
    loan_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="loans")
    copy = models.ForeignKey("copies.Copies", on_delete=models.CASCADE)
