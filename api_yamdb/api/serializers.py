from rest_framework import serializers
from reviews.models import Comment, Review, Genre, Category, Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ("id", "name", "year", "rating", "description",
                  "category", "genre")
        model = Title
        read_only_fields = ("id", "rating")


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(), slug_field="slug"
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ("id", "name", "year", "rating", "description",
                  "category", "genre")
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, data):
        is_exist = Review.objects.filter(
            author=self.context["request"].user,
            title=self.context["view"].kwargs.get("title_id"),
        ).exists()
        if is_exist and self.context["request"].method == "POST":
            raise serializers.ValidationError(
                "Пользователь уже оставлял отзыв на это произведение"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
