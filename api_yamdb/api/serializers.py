from rest_framework import serializers
from reviews.models import (Title, Category,
                            Genre, User,
                            Review, Comment)
from reviews.validators import validate_username
from rest_framework.validators import UniqueValidator


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug',
                                         many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:
        model = Title
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

        # Атрибут списка поля, который стоит скорее всего исключить
        # для нормальной работы

        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre

        # Атрибут списка поля, который стоит скорее всего исключить
        # для нормальной работы

        exclude = ['id']


class TitleObjectsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ['id', 'name',
                  'year', 'description',
                  'genre', 'category', 'rating']


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')


class OwnerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())],
        required=True)

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review

        # Атрибут списка поля, который стоит скорее всего исключить
        # для нормальной работы

        exclude = ['title']
        read_only_fields = ('id', 'author', 'pub_date')

    def validate(self, data):

        # проверка на укникальность отзыва по юзеру и айди тайтла

        if self.context['request'].method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            user = self.context['request'].user
            if Review.objects.filter(title_id=title_id, author=user).exists():
                raise serializers.ValidationError(
                    'U have done with that already')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment

        # Атрибут списка поля, который стоит скорее всего исключить
        # для нормальной работы

        exclude = ['review']
        read_only_fields = ('id', 'author', 'pub_date')


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,
                                     validators=[validate_username, ],
                                     required=True)
    email = serializers.EmailField(required=True, max_length=254)

    def validate(self, data):
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if (User.objects.filter(username=data['username']).exists()
                or User.objects.filter(email=data['email']).exists()):
            raise serializers.ValidationError(
                'User with thats nickname and email done already'
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,
                                     validators=[validate_username, ],
                                     required=True)

    # Тот самый токен

    confirmation_code = serializers.CharField(required=True)
