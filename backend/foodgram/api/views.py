from django.contrib.auth import get_user_model
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import AllowAny

from . serializers import (TagSerializer, IngredientSerializer,
                           RecipesSerializer, FavoriteSerializer,
                           ShoppingCartSerializer)
from . models import Ingredient, Reciepes, Tag
from . permissions import IsAuthorOrReadOnly
from . filters import IngredientSearchFilter, RecipeFilter
from .pagination import CustomPageNumberPagination


codegen = PasswordResetTokenGenerator()
User = get_user_model()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
 

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)


class ReciepesViewSet(viewsets.ModelViewSet):
    queryset = Reciepes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Reciepes.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = Reciepes.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthorOrReadOnly,)
