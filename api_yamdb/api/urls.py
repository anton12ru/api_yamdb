from django.urls import include, path
from rest_framework import routers

from api.views import (CommentViewSet, CustomUserViewSet,
                       RegisterCustomUserViewSet, ReviewViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'auth/signup/', RegisterCustomUserViewSet, basename='signup')
router_v1.register(r'users/', CustomUserViewSet)
# router_v1.register
# router_v1.register
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
