from django.urls import path
from .views import BookDetailView, BookListLatest, BookView

urlpatterns = [
    path("books/<int:pk>/", BookDetailView.as_view()),
    path("books/", BookView.as_view()),
    path("books/latest/", BookListLatest.as_view()),
]
