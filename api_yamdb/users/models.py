from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLE = (
    (ADMIN, 'admin'),
    (MODERATOR, 'moderator'),
    (USER, 'user')
)


class CustomUser(AbstractUser):

    bio = models.TextField(blank=True, null=True)
    role = models.CharField(choices=ROLE, max_length=50)

    @property
    def is_user(self):
        return ROLE == USER

    @property
    def is_moderator(self):
        return ROLE == MODERATOR

    @property
    def is_admin(self):
        return ROLE == ADMIN
