from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . views import (IngredientViewSet, ReciepesViewSet, TagViewSet,
                    RegisterUserAPIView, GetTokenAPIView, UsersViewSet,
                    FavoriteViewSet, ShoppingCartViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename = 'ingredients')
router.register('reciepes', ReciepesViewSet, basename = 'reciepes')
router.register('tags', TagViewSet, basename = 'tags')
router.register('users', UsersViewSet)
router.register(r'reciepes/(?P<id>\d+)/favorite', 
                FavoriteViewSet, basename = 'favorite')
router.register(r'reciepes/(?P<id>\d+)/shopping_cart', 
                ShoppingCartViewSet, basename = 'shopping_cart')

auth_urls_v1 = [
    path('auth/signup/', RegisterUserAPIView.as_view(), name='signup'),
    path('auth/token/', GetTokenAPIView.as_view(), name='get_token'),
]


urlpatterns = [
    path('api/', include(auth_urls_v1)),
    path('api/', include(router.urls)),
]
