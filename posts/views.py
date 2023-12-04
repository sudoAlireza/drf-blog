from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .models import Post, Rating
from .serializers import PostSerializer, RatingSerializer


class PostListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
            )

        data = {
            "title": request.data.get("title"),
            "body": request.data.get("body"),
            "user": request.user.id,
        }
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user = request.user
        posts = Post.objects.all()

        serialized_posts = []

        for post in posts:
            average_rating = post.ratings.aggregate(models.Avg("rate"))["rate__avg"]
            user_rating = (
                Rating.objects.filter(user=user, post=post).values("rate").first()
            )
            rating_count = (
                Rating.objects.filter(post=post).values("user").distinct().count()
            )
            serialized_post = {
                "id": post.id,
                "title": post.title,
                "body": post.body,
                "user": post.user.id,
                "average_rating": average_rating if average_rating else 0.0,
                "current_user_rating": user_rating["rate"] if user_rating else None,
                "rating_count": rating_count,
            }

            serialized_posts.append(serialized_post)

        return Response(serialized_posts, status=status.HTTP_200_OK)


class RatePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=post_id)

        existing_rating = Rating.objects.filter(user=user, post=post).first()

        if existing_rating:
            serializer = RatingSerializer(existing_rating, data=request.data)
        else:
            data = {"user": user.id, "post": post.id, "rate": request.data.get("rate")}
            serializer = RatingSerializer(data=data)

        if serializer.is_valid():
            serializer.save(user=user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
