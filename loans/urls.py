from django.urls import path
from .views import LoanView, LoanReturnView

urlpatterns = [
    path("loans/", LoanView.as_view()),
    path("loans/<int:pk>/", LoanReturnView.as_view()),
]
