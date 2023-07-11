from django.urls import path
from .views import CopyView, CopyDetailView, BookFollowView, BookListFollowersView, BookUnfollowView

urlpatterns = [
    path("copies/", CopyView.as_view()),
    path("copies/<int:pk>/", CopyDetailView.as_view()),
    path("copies/<int:pk>/follow/", BookFollowView.as_view()),
    path("copies/followers/", BookListFollowersView.as_view()),
    path("copies/<int:pk>/unfollow/", BookUnfollowView.as_view()),
]
