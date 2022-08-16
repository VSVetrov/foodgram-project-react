from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from api.models import Recipe

from .models import Follow

User = get_user_model()


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user.id
        queryset = Follow.objects.filter(
            user=request_user, author=obj.id
        ).exists()
        return queryset


class UserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password'
        )


class RecipeSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = RecipeSubscriptionSerializer(
        many=True
    )
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        )
        read_only_fields = ('__all__',)

    def to_representation(self, instance):
        recipes = RecipeSubscriptionSerializer(
            instance=instance.recipes,
            many=True
        ).data
        recipes_limit_data = self.context.get('request').query_params
        data = super(SubscriptionSerializer, self).to_representation(instance)
        if 'recipes_limit' in recipes_limit_data:
            recipes_limit = int(recipes_limit_data['recipes_limit'])
            data['recipes'] = recipes[:recipes_limit]
            return data
        data['recipes'] = recipes
        return data

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user.id
        queryset = Follow.objects.filter(
            user=request_user, author=obj.id
        ).exists()
        return queryset

    def get_recipes_count(self, obj):
        return obj.recipes.count()
