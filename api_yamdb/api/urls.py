from django.urls import path, include
from rest_framework import routers

from api.views import ReviewViewSet, CommentViewSet

router_v1 = routers.DefaultRouter
router_v1.register(
    r'titles/(?P<post_id>\d+)/reviews/', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<post_id>\d+)/reviews/(?P<post_id>\d+)/comments/',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
