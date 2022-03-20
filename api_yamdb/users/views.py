from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, views
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination

from users.models import CustomUser
from users.serializers import (
    CustomUserSerializer,
    LoginTokenSerializer,
    RegistrationUserSerializer,
)


def send_mail_confirmation_code(user):
    """создаем код подтверждения и отправляем по email"""
    confirmation_code = default_token_generator.make_token(user)
    subject = "Confirmation code"
    message = f"{confirmation_code}, ваш код для получения Token"
    from_email = "from@example.com"
    to_email = [user.email]
    return send_mail(subject, message, from_email, to_email)


class RegistrationUserAPIView(views.APIView):
    serializer_class = RegistrationUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """Получаем confirmation_code в конссоль при POST запросе.
        С данными username и email.
        """
        serializer = RegistrationUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_mail_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginTokenAPIView(views.APIView):
    serializer_class = LoginTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """Делаем POST запрос с username и confirmation_code.
        И получаем Token для аутентификации пользователя.
        """
        serializer = LoginTokenSerializer(data=request.data)
        if serializer.is_valid() is None:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.data["username"]
        confirmation_code = serializer.data["confirmation_code"]
        user = CustomUser.object.get(username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        return Response({"token": str(token.access_token)}, status=status.HTTP_200_OK)


class CustomUserAPIView(views.APIView):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = CustomUser.object.all()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def putch(self, request):
        serializer = CustomUserSerializer(request.user)
        if request.method == "PATCH":
            serializer = CustomUserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminUserViewSet(ModelViewSet):
    queryset = CustomUser.object.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = LimitOffsetPagination
