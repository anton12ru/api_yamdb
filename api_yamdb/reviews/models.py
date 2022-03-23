from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser

from .validators import year_validator


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        unique=True,
        max_length=20,
        verbose_name="Часть URL адреса группы",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название жанра",
    )
    slug = models.SlugField(
        unique=True,
        max_length=20,
        verbose_name="Часть URL адреса группы",
    )


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название произведения",
    )
    year = models.PositiveSmallIntegerField(
        validators=[year_validator],
        help_text="Используйте формат ввода года выпуска: <YYYY>",
        verbose_name="Год",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание произведения",
    )
    genre = models.ManyToManyField(Genre, related_name="titles", blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("-year",)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("title", "author"), name="unique_title_author"
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
