import datetime
from django.core.exceptions import ValidationError


def year_validator(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            f"{value}год - не может быть больше текущего года"
        )
