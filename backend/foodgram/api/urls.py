from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, ReciepesViewSet, TagViewSet

app_name = 'api'

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename = 'ingredients')
router.register('reciepes', ReciepesViewSet, basename = 'recipes')
router.register('tags', TagViewSet, basename = 'tags')


urlpatterns = [
    path('api/', include(router.urls)),
]
