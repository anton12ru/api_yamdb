from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Title(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="titles"
    )
    genre = models.ManyToManyField(
        Genre, on_delete=models.SET_NULL, related_name="titles"
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    year = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, blank=True, null=True)


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    score = models.IntegerField(
        validators=(MinValueValidator[1], MaxValueValidator[10]), blank=True
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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
