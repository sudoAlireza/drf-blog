# urls.py
from django.urls import path
from .views import PostListAPIView, RatePostView

urlpatterns = [
    path("", PostListAPIView.as_view()),
    path("<int:post_id>/rate/", RatePostView.as_view(), name="rate-post"),
]
