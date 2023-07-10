from django.urls import path
from .views import CreateReviewView, ListReviewView, ReviewDetailView


urlpatterns = [
    path("review/create/<int:pk>/", CreateReviewView.as_view()),
    path("review/", ListReviewView.as_view()),
    path("review/<int:pk>/", ReviewDetailView.as_view()),
]
