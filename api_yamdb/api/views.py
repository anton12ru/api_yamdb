from django.db.models import Avg
from rest_framework import viewsets, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.filters import TitleFilter
from reviews.models import Category, Genre, Review, Title
from api.permissions import IsAdminOrAuthorOrReadOnly, IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from api.mixins import ListCreateDestroyViewSet
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleWriteSerializer,
)


class GenreViewSet(ListCreateDestroyViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=name",)


class CategoryViewSet(ListCreateDestroyViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=name",)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(
            Review, id=self.kwargs.get("review_id", "title_id")
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs.get("review_id", "title_id")
        )
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    ordering_fields = ("name",)
    filterset_fields = ("=genre__slug",)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleSerializer
        return TitleWriteSerializer
