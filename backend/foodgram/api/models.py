from django.db import models
from django.conf import settings
from django.utils.html import format_html
from django.core.validators import MinValueValidator

from users.models import User

class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.color,
        )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.username


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    amount = models.IntegerField()
    measurement_unit = models.IntegerField()

    def __str__(self):
        return self.username


class Reciepes(models.Model):
    author = models.CharField(User, max_length=150, unique=True)
    name = models.CharField(
        max_length=256,
        unique=True,
        help_text='Назовите блюдо')
    image = models.ImageField(help_text='Добавьте картинку')
    text = models.TextField(help_text='Запишите рецепт')
    ingredients = models.ForeignKey(
        Ingredient,
        related_name='ingredients',
        on_delete=models.CASCADE,
        help_text='Выберите состав блюда')
    tags = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tags')
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                1, message='Время должно быть больше 1 минуты'),),
            help_text='Время приготовления в минутах')

    def __str__(self):
        return self.username
