from rest_framework import serializers, validators

from users.models import CustomUser


class RegistrationUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, validators=[
        validators.UniqueValidator(
            queryset=CustomUser.object.all()
        )
    ])
    email = serializers.EmailField(max_length=50, validators=[
        validators.UniqueValidator(
            queryset=CustomUser.object.all()
        )
    ])

    class Meta:
        model = CustomUser
        fields = ("username", "email")

    def validate_me(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Использовать 'me' в качестве username запрещено!!!"
            )


class LoginTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    confirmation_code = serializers.CharField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ("username", "confirmation_code")


class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    username = serializers.CharField(max_length=150, validators=[
        validators.UniqueValidator(
            queryset=CustomUser.object.all()
        )
    ])
    email = serializers.EmailField(max_length=254, validators=[
        validators.UniqueValidator(
            queryset=CustomUser.object.all()
        )
    ])

    class Meta:
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )
        model = CustomUser

    def validate_me(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Использовать 'me' в качестве username запрещено!!!"
            )
