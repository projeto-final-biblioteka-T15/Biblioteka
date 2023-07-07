from django.db import models
from books.models import Book
from loans.models import Loan
from django.core.mail import send_mail
from users.models import User
from django.conf import settings


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
        

    def return_copy(self):
        self.available += 1
        self.save()

        loan = Loan.objects.filter(copy=self, returned=False).first()
        if loan:
            loan.returned = True
            loan.save()
            self.check_user_blocked(loan.user)
        
        
        if self.available == 1:            
            followers = BookFollower.objects.filter(book=self.book)            
            for follower in followers:
                send_mail(
                    from_email=settings.EMAIL_HOST_USER,
                    subject="Novo livro disponível",
                    message=f"O livro {self.book.title} está disponível",
                    recipient_list=[follower.user.email],
                    fail_silently=False,
                )

