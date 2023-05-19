from django.contrib.auth.models import AbstractUser
from django.db import models
from reviews.validators import validate_username


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (USER, "USER"),
        (ADMIN, "ADMIN"),
        (MODERATOR, "MODERATOR"),
    ]
    email = models.EmailField('Email', max_length=254, unique=True)
    username = models.CharField('username', max_length=150, unique=True, validators=[validate_username])
    role = models.CharField('Role', max_length=50, choices=ROLES, default=USER)
    first_name = models.CharField('First Name', max_length=150, blank=True)
    bio = models.TextField('Bio', null=True, blank=True)
    confirmation_code = models.CharField(
        'confirmation code',
        max_length=254,
        null=True,
        blank=True,
        default='None'
    )


    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
