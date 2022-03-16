from rest_framework.viewsets import ModelViewSet
from reviews.models import Comment, Review
from users.models import CustomUser

from api.serializers import (CommentSerializer, CustomUserSerializer,
                             RegisterCustomUserSerializer, ReviewSerializer)


class CustomUserViewSet(ModelViewSet):
    class_serializer = CustomUserSerializer
    queryset = CustomUser.objects.all()


class RegisterCustomUserViewSet(ModelViewSet):
    class_serializer = RegisterCustomUserSerializer


class ReviewViewSet(ModelViewSet):
    class_serializer = ReviewSerializer
    queryset = Review.objects.all()


class CommentViewSet(ModelViewSet):
    class_serializer = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        queryset = Comment.objects.filter(review=review_id)
        return queryset
