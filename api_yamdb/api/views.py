from rest_framework.viewsets import ModelViewSet

from api.serializers import ReviewSerializer, CommentSerializer
from reviews.models import Review, Comments


class ReviewViewSet(ModelViewSet):
    class_serializer = ReviewSerializer
    queryset = Review.objects.all()


class CommentViewSet(ModelViewSet):
    class_serializer = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        queryset = Comments.objects.filter(review=review_id)
        return queryset
