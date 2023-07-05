from django.db import models


class Loan(models.Model):

    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(auto_now_add=True)
    
    copy = models.ForeignKey("copies.Copies", on_delete=models.CASCADE, related_name="loans")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="loans")
