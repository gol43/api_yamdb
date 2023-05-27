from django.db import models
from reviews.validators import validate_year, validate_username
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Name of category",
        unique=True)
    slug = models.SlugField(
        max_length=50,
        verbose_name="Slug for category",
        unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Name of genre",
        unique=True)
    slug = models.SlugField(
        max_length=50,
        verbose_name="Slug for genre",
        unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Name of title")
    year = models.IntegerField(
        verbose_name="Year for title",
        validators=[validate_year, ])
    description = models.TextField(verbose_name="Des for title")
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Slug of genre")
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Slug of category")

    def __str__(self):
        return self.name


class User(AbstractUser):

    # https://docs.djangoproject.com/en/4.2/ref/models/fields/
    # models.TextChoices взято отсюда

    class RoleChoices(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    username = models.CharField(
        'Nickname for user',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[validate_username, ])
    email = models.EmailField(
        'Email for user',
        max_length=254,
        unique=True,
        blank=False,
        null=False)
    first_name = models.CharField(
        'Name of user',
        max_length=150,
        blank=True)
    last_name = models.CharField(
        "Surname of user",
        max_length=150,
        blank=True)
    bio = models.TextField(
        'BIO of user',
        blank=True,)
    role = models.CharField(
        'Role',
        max_length=50,
        choices=RoleChoices.choices,

        # Используйте .choices в качестве
        # подходящего значения для перехода в choicesопределение поля

        default=RoleChoices.USER)

    def __str__(self):
        return self.username


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Reviews')
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[

            # integer (Оценка) [ 1 .. 10 ]

            MinValueValidator(1, 'Error'),
            MaxValueValidator(10, 'Error')])
    pub_date = models.DateTimeField(
        verbose_name='Pub_date',
        auto_now_add=True)

    class Meta:

        #  Проверьте, что на уровне модели запрещено повторное создание
        #  отзыва на произведение от имени пользователя,
        #  отзыв которого уже существует.

        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_reviews')]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class GenreTitle(models.Model):
    # добавил для csv_files:
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Genre-Title'

    def __str__(self):
        return self.genre and self.title
