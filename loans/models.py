from django.db import models
from django.utils import timezone
from datetime import timedelta


class Loan(models.Model):
    loan_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    return_made = models.DateField(null=True, blank=True)
    
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="loans")
    copy = models.ForeignKey("copies.Copies", on_delete=models.CASCADE)
    
    def check_return_date(self):
        if self.return_made and self.return_made > self.return_date:
            self.user.is_blocked = True
            self.user.blocked_until = timezone.now().date() + timezone.timedelta(days=7)
            self.user.save()

