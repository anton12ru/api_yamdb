from rest_framework import serializers

from users.models import CustomUser


class RegistrationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class LoginTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    confirmation_code = serializers.CharField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ("username", "confirmation_code")
