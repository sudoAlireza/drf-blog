from rest_framework import serializers
from .models import Post, Rating


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "body")


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["user", "post", "rate"]
        extra_kwargs = {"user": {"read_only": True}}
