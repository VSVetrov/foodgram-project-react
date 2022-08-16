from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

from .views import IngredientViewSet, RecipesViewSet, TagViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'recipes', RecipesViewSet, basename='recipe')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
