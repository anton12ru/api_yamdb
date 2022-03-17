from django.urls import path

from .views import LoginTokenAPIView, RegistrationUserAPIView

urlpatterns = [
    path("signup/", RegistrationUserAPIView.as_view()),
    path("token/", LoginTokenAPIView.as_view()),
]
