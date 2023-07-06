from django.db import models
from books.models import Book
from django.utils import timezone
from loans.models import Loan
from datetime import timedelta
from django.core.mail import send_mail
from users.models import User


class BookFollower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


class Copies(models.Model):
    total = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)

    book = models.ForeignKey(Book, related_name="copies", on_delete=models.CASCADE)

    def loan_copy(self):
        if self.available > 0:
            self.available -= 1
            self.save()
        else:
            raise Exception("Não há cópias disponíveis para empréstimo.")

    def notify_followers(self):
        if self.available > 0:
            followers = BookFollower.objects.filter(book=self.book)
            for follower in followers:
                send_mail(
                    "Novo livro disponível",
                    f"O livro {self.book.title} está disponível",
                    [follower.user.email],
                    fail_silently=False,
                )

    def return_copy(self):
        self.available += 1
        self.save()

        loan = Loan.objects.filter(copy=self, returned=False).first()
        if loan:
            loan.returned = True
            loan.save()
            self.check_user_blocked(loan.user)

        self.notify_followers()

    def check_user_blocked(self, user):
        loans_pending = Loan.objects.filter(
            user=user, returned=False, return_date__lt=timezone.now()
        ).exists()

        if loans_pending:
            user.is_blocked = True
            user.blocked_until = timezone.now() + timedelta(days=7)
            user.save()
