from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, username, email, role, **extra_fields):
        if username is None:
            raise ValueError("Поле username обязательное!")
        if email is None:
            raise ValueError("Поле email обязательное!")
        return super().create_user(username, email, role, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        if password is None:
            raise TypeError("Поле password обязательное!")
        return super().create_superuser(username, email,
                                        password, **extra_fields)


class CustomUser(AbstractUser):

    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

    ROLE = ((ADMIN, "admin"), (MODERATOR, "moderator"), (USER, "user"))

    email = models.EmailField(
        max_length=50, unique=True, blank=False, null=False)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(choices=ROLE, max_length=50, default="user")
    object = CustomUserManager()

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
