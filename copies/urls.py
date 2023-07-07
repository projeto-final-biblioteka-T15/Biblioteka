from django.urls import path
from .views import CopyView, CopyDetailView, BookFollowView

urlpatterns = [
    path("copies/", CopyView.as_view()),
    path("copies/<int:pk>/", CopyDetailView.as_view()),
    path("copies/<int:pk>/follow/", BookFollowView.as_view()),
]
