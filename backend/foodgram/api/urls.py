from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . views import (IngredientViewSet, ReciepesViewSet, TagViewSet,
                    FavoriteViewSet, ShoppingCartViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename = 'ingredients')
router.register('reciepes', ReciepesViewSet, basename = 'reciepes')
router.register('tags', TagViewSet, basename = 'tags')
router.register(r'reciepes/(?P<id>\d+)/favorite', 
                FavoriteViewSet, basename = 'favorite')
router.register(r'reciepes/(?P<id>\d+)/shopping_cart', 
                ShoppingCartViewSet, basename = 'shopping_cart')


urlpatterns = [
    path('api/', include(router.urls)),
]
