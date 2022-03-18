from rest_framework.viewsets import ModelViewSet
from reviews.models import Comment, Review, Genre, Category
from users.models import CustomUser

from api.serializers import (
    CommentSerializer,
    CustomUserSerializer,
    RegisterCustomUserSerializer,
    ReviewSerializer,
    GenreSerializer,
    CategorySerializer,
)

class GenreViewSet(ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CustomUserViewSet(ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class RegisterCustomUserViewSet(ModelViewSet):
    serializer_class = RegisterCustomUserSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        queryset = Comment.objects.filter(review=review_id)
        return queryset
