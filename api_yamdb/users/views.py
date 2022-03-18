from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser
from users.serializers import LoginTokenSerializer, RegistrationUserSerializer


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
        username = serializer.data["username"]
        confirmation_code = serializer.data["confirmation_code"]
        user = CustomUser.object.get(username=username)
        if not (
            serializer.is_valid()
            or default_token_generator.check_token(user, confirmation_code)
        ):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(token=None, verify=True)
        return Response(str(token.access_token), status=status.HTTP_200_OK)
