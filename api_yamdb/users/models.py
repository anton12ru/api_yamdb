from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

ADMIN = "admin"
MODERATOR = "moderator"
USER = "user"

ROLE = ((ADMIN, "admin"), (MODERATOR, "moderator"), (USER, "user"))


class CustomUserManager(UserManager):
    def create_user(self, username, email, **extra_fields):
        if username is None:
            raise ValueError("Поле username обязательное!")
        if username == "me":
            raise ValueError('Имя пользователя "me" нельзя использовать!')
        if email is None:
            raise ValueError("Поле email обязательное!")
        return super().create_user(username, email, **extra_fields)

    def create_superuser(self, username, email, password, role, **extra_fields):
        role = ADMIN
        if password is None:
            raise TypeError("Поле password обязательное!")
        return super().create_superuser(username, email, password, role, **extra_fields)


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True, blank=False, null=False)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(choices=ROLE, max_length=50)

    object = CustomUserManager()

    @property
    def is_user(self):
        return ROLE == USER

    @property
    def is_moderator(self):
        return ROLE == MODERATOR

    @property
    def is_admin(self):
        return ROLE == ADMIN
