from django.urls import path
from .views import CreateReviewView
from .views import ListReviewView


urlpatterns = [
    path("review/<int:pk>/", CreateReviewView.as_view()),
    path("review/", ListReviewView.as_view()),
]
