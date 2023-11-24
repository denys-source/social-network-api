from rest_framework import serializers

from social_app.models import Like, Post
from user.serializers import UserSerializer


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "user",)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "text")


class PostListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "text",
            "created_at",
            "updated_at",
            "user",
            "likes_count",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes = LikeSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "text",
            "created_at",
            "updated_at",
            "user",
            "likes",
        )
