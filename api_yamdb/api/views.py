from rest_framework.viewsets import ModelViewSet
from reviews.models import Category, Comment, Genre, Review

from .mixins import CreateDestroyListViewSet
from .permissions import AdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer)


class GenreViewSet(CreateDestroyListViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (AdminOrReadOnly,)


class CategoryViewSet(CreateDestroyListViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (AdminOrReadOnly,)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        queryset = Comment.objects.filter(review=review_id)
        return queryset
