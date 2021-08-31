from rest_framework.routers import DefaultRouter

from django.conf.urls import include
from django.urls import path

from .views import (
    IngredientViewSet, TagViewSet, shoppinglist,
    RecipeViewSet, favourite, subscription,
)
from .utils import download_shopping_list

router_v1 = DefaultRouter()

router_v1.register('ingredients', IngredientViewSet)
router_v1.register('tags', TagViewSet)
router_v1.register('recipes', RecipeViewSet)

urlpatterns = [
    path('users/<int:id>/subscribe/',
         subscription,
         name='user_subscription'),
    path('recipes/<int:recipe_id>/favorite/',
         favourite,
         name='recipe_favourite'),
    path('recipes/<int:id>/shopping_cart/',
         shoppinglist,
         name='making_the_cart'),
    path('recipes/download_shopping_cart/',
         download_shopping_list,
         name='dsc'),
    path('', include(router_v1.urls)),
]
