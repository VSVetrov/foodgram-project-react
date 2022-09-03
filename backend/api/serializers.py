from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True, source='ingredientsamount'
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart', 'name',
            'image', 'text', 'cooking_time'
        )
        read_only_fields = ('id', 'author')

    def validate(self, data):
        ingredients = data['ingredientsamount']
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': ('Добавьте хотя бы один ингредиент')})
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredient,
                id=ingredient_item['ingredient']['id']
            )
            if int(ingredient_item('amount')) <= 0:
                raise serializers.ValidationError(
                        'Убедитесь, что значение '
                        'количества ингредиента больше 0'
                    )
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиенты должны быть уникальными'
                )
            ingredient_list.append(ingredient)
            data['ingredients'] = ingredients
        return data

    def create_ingredients(self, recipe, ingredients):
        IngredientAmount.objects.bulk_create([
            IngredientAmount(
                recipe=recipe,
                ingredient_id=ingredient['ingredient']['id'],
                amount=ingredient['amount'],
            ) for ingredient in ingredients
        ])

    def create(self, validated_data):
        validated_data.pop('ingredients', {})
        ingredients = validated_data.pop('ingredientsamount', {})
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        del validated_data['ingredients']
        instance.tags.clear()
        instance.tags.set(validated_data.pop('tags'))
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.create_ingredients(
            recipe=instance,
            ingredients=validated_data.pop('ingredientsamount')
        )
        super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        data = super(
            RecipeSerializer, self).to_representation(instance)
        data['tags'] = TagSerializer(
            instance.tags, many=True, required=False).data
        return data

    def get_is_favorited(self, obj):
        request_user = self.context.get('request').user.id
        return Favorite.objects.filter(
            user=request_user, recipe=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request_user = self.context.get('request').user.id
        return ShoppingCart.objects.filter(
            user=request_user, recipe=obj.id
        ).exists()


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientAmountSerializer(
        many=True, source='ingredientsamount')
    author = UserSerializer(required=False, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        favorite = Favorite.objects.filter(
            user=user.id,
            recipe=obj.id
        )
        return favorite.exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        shopping = ShoppingCart.objects.filter(
            user=user.id,
            recipe=obj.id
        )
        return shopping.exists()


class FavoriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('__all__',)
