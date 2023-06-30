from django.urls import path

# from . import views

from loans import views as loan_views

urlpatterns = [
    path("loans/", loan_views.LoanView.as_view()),
    path("loans/<int:pk>/", loan_views.LoanView.as_view())
]
