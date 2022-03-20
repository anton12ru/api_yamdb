from django.urls import include, path
from rest_framework import routers

from users.views import CustomUserAPIView, AdminUserViewSet
from api.views import CommentViewSet, ReviewViewSet, GenreViewSet, CategoryViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r"users", AdminUserViewSet)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/", include("users.urls")),
    path("v1/users/me/", CustomUserAPIView.as_view()),
]
