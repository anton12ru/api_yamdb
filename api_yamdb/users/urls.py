from django.urls import path

from .views import LoginTokenAPIView, RegistrationUserAPIView

urlpatterns = [
    path("auth/signup/", RegistrationUserAPIView.as_view()),
    path("auth/token/", LoginTokenAPIView.as_view()),
]
