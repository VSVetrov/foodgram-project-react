from rest_framework import serializers

from . models import Ingredient, Reciepes, Tag
#from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.SlugRelatedField(slug_field='slug')

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    amount = serializers.IntegerField() 

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__'


class RecipesSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    #author = CustomUserSerializer(read_only=True)
    cooking_time = serializers.IntegerField()
    
    class Meta:
        model = Reciepes
        fields = '__all__'


    def validate(self, data):
        ingredients = data['ingredients']
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError({
                    'ingredients': 'Ингредиенты должны быть уникальными!'
                })
            ingredients_list.append(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError({
                    'amount': 'Количество ингредиента должно быть больше нуля!'
                })

        tags = data['tags']
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Нужно выбрать хотя бы один тэг!'
            })
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError({
                    'tags': 'Тэги должны быть уникальными!'
                })
            tags_list.append(tag)

        cooking_time = data['cooking_time']
        if int(cooking_time) <= 0:
            raise serializers.ValidationError({
                'cooking_time': 'Время приготовления должно быть больше 0!'
            })
        return data


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reciepes
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    cooking_time = serializers.IntegerField()
    
    class Meta:
        model = Reciepes
        fields =('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if Reciepes.objects.filter(user=request.user, recipe=recipe).exists():
            raise serializers.ValidationError({
                'status': 'Рецепт уже есть в избранном!'
            })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe, context=context).data



class ShoppingCartSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    cooking_time = serializers.IntegerField()
    
    class Meta:
        model = Reciepes
        fields =('id', 'name', 'image', 'cooking_time')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe, context=context).data
