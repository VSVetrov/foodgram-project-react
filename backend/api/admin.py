from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


class MinValidatedInlineMixIn:
    validate_min = True

    def get_formset(self, *args, **kwargs):
        return super().get_formset(validate_min=self.validate_min,
                                   *args, **kwargs)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientAmountAdmin(MinValidatedInlineMixIn, admin.TabularInline):
    model = IngredientAmount
    min_num = 1
    validate_min = True
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'amount_favorites',
                    'amount_tags', 'amount_ingredients', 'ingredients')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)
    inlines = [IngredientAmountAdmin, ]
    exclude = ['ingredients']
    empty_value_display = '-пусто-'

    @staticmethod
    def amount_favorites(obj):
        return obj.favorites.count()

    @staticmethod
    def amount_tags(obj):
        return '\n'.join([i[0] for i in obj.tags.values_list('name')])

    @staticmethod
    def amount_ingredients(obj):
        return '\n'.join([i[0] for i in obj.ingredients.values_list('name')])


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = '-пусто-'
