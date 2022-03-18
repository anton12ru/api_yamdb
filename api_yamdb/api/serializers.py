from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reviews.models import Comment, Review
from users.models import ROLE, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE)

    class Meta:
        fields = ("username", "email", "first_name", "last_name", "bio", "role")
        model = CustomUser


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fileds = ("id", "text", "author", "pub_date")
        model = Comment
