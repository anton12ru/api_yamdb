from rest_framework.viewsets import ModelViewSet
from reviews.models import Comment, Review

from api.serializers import (
    CommentSerializer,
    ReviewSerializer,
)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        queryset = Comment.objects.filter(review=review_id)
        return queryset
