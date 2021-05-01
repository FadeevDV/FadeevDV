from django.db import models


class Category(models.Model):
    name = models.CharField('Название', max_length=20)
    slug = models.SlugField('Адрес', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=20)
    slug = models.SlugField('Адрес', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=20)
    year = models.PositiveSmallIntegerField('Год выпуска')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 verbose_name='Категория',
                                 blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр', related_name='titles'
    )
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name
