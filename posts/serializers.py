from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="username",
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "text",
            "pub_date",
            "author",
            "image",
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="username",
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "post",
            "text",
            "created",
        )
