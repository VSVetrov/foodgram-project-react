# Generated by Django 2.2.16 on 2022-08-11 04:08

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Назовите блюдо', max_length=256, unique=True)),
                ('image', models.ImageField(help_text='Добавьте картинку', upload_to='recipes/', verbose_name='Картинка рецепта')),
                ('text', models.TextField(help_text='Запишите рецепт')),
                ('cooking_time', models.PositiveSmallIntegerField(help_text='Время приготовления в минутах', validators=[django.core.validators.MinValueValidator(1, message='Время должно быть больше 1 минуты')])),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(help_text='Выберите состав блюда', related_name='recipes', to='api.Ingredient')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('color', models.CharField(max_length=7, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='api.Recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзина',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='api.Tag'),
        ),
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Количество не может быть меньше 1')], verbose_name='Количество ингредиента')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredientsamount', to='api.Ingredient', verbose_name='Ингредиент')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredientsamount', to='api.Recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Количество ингредиента',
                'verbose_name_plural': 'Количество ингредиентов',
            },
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique ingredient'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='api.Recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique shopping cart'),
        ),
        migrations.AddConstraint(
            model_name='ingredientamount',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique ingredient amount'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique favorite'),
        ),
    ]
