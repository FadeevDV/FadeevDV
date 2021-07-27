from django.contrib.auth import get_user_model

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Категория произведения'
    )
    slug = models.SlugField(
        null=False,
        blank=False,
        unique=True,
        verbose_name='slug категории произведения'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Жанр произведения'
    )
    slug = models.SlugField(
        null=False,
        blank=False,
        unique=True,
        verbose_name='slug жанра произведения'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='Название произведения'
    )
    year = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name='Год создания произведения'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Рейтинг не может быть ниже 1'),
            MaxValueValidator(10, 'Рейтинг не может быть выше 10'),
        ],
        null=True,
        verbose_name="Рейтинг",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name
