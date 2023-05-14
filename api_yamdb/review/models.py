from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Name for genre',)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name='URL of group',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Name for category',)
    slug = models.SlugField(
        max_length=20,
        verbose_name='URL for group',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Name for title',)
    description = models.TextField(
        max_length=1000,
        verbose_name='Description for title',)
    year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Year")
    genre = models.ManyToManyField(
        Genre, related_name='titles',)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',)

    def __str__(self):
        return self.name
