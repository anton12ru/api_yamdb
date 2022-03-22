from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, views
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import AdminOnlyPermission
from users.models import CustomUser
from users.serializers import (CustomUserSerializer, LoginTokenSerializer,
                               RegistrationUserSerializer)


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
        email = request.data.get('email')
        username = request.data.get('username')

        if serializer.is_valid():
            user = CustomUser.objects.filter(
                email=email, username=username)
            print(user)

            if not user.exists():
                new_user = CustomUser.objects.create(
                    email=email, username=username)
                send_mail_confirmation_code(new_user)
                return Response(serializer.data, status=status.HTTP_200_OK)

            send_mail_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginTokenAPIView(views.APIView):
    serializer_class = LoginTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """Делаем POST запрос с username и confirmation_code.
           И получаем Token для аутентификации пользователя.
        """
        serializer = LoginTokenSerializer(data=request.data)
        if not serializer.is_valid() or None:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.data["username"]
        confirmation_code = serializer.data["confirmation_code"]
        user = get_object_or_404(CustomUser, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        return Response(
            {"token": str(token.access_token)}, status=status.HTTP_200_OK)


class CustomUserAPIView(views.APIView):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(CustomUser, username=request.user.username)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def putch(self, request):
        user = get_object_or_404(CustomUser, username=request.user.username)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminUserViewSet(ModelViewSet):
    queryset = CustomUser.object.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AdminOnlyPermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
