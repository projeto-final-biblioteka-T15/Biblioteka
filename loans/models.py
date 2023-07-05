from django.db import models

from django.utils import timezone

# class Loan(models.Model):

#     loan_date = models.DateField(auto_now_add=True)
#     return_date = models.DateField(auto_now_add=True)

#     copy = models.ForeignKey("copies.Copies", on_delete=models.CASCADE, related_name="loans")
#     user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="loans")


class Loan(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="loans"
    )
    copy = models.ForeignKey("copies.Copies", on_delete=models.CASCADE)
    loan_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)
