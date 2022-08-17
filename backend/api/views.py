from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientSearchFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeListSerializer, RecipeSerializer,
                          TagSerializer)

User = get_user_model()

SHOPPING_LIST_FORMAT = '{name} {measurement_unit} - {total_amount}'
SHOPPING_LIST_FILE_NAME = 'Список покупок'


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


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    ordering_fields = ('id',)
    ordering = ('-id',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def favorite_shopping_cart(
        self,
        request,
        used_model,
        used_serializer,
        id,
        error_message
    ):
        recipe = get_object_or_404(Recipe, id=id)
        if request.method == "POST":
            if_already_exists = used_model.objects.filter(
                user=request.user, recipe=recipe
            ).exists()
            if if_already_exists:
                return Response(
                    {'errors': error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )
            used_model.objects.create(user=request.user, recipe=recipe)
            serializer = used_serializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(
                used_model,
                user=request.user,
                recipe=recipe
            )
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        error_message = 'Рецепт уже добавлен в избранное'
        return self.favorite_shopping_cart(
            request=request,
            used_model=Favorite,
            used_serializer=FavoriteSerializer,
            id=pk,
            error_message=error_message
        )

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        error_message = 'Рецепт уже добавлен в корзину'
        return self.favorite_shopping_cart(
            request=request,
            used_model=ShoppingCart,
            used_serializer=FavoriteSerializer,
            id=pk,
            error_message=error_message
        )

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_list = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            name=F('ingredient__name'),
            measurement_unit=F('ingredient__measurement_unit')
        ).annotate(total_amount=Sum('amount'))
        text = '\n'.join([
            SHOPPING_LIST_FORMAT.format(
                name=item['name'],
                measurement_unit=item['measurement_unit'],
                total_amount=item['total_amount']
            )
            for item in shopping_list
        ])
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; '
            f'filename={SHOPPING_LIST_FILE_NAME}'
        )
        return response
