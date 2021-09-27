from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, filters

from users.models import User
from .models import (
    Recipe, Shoppinglist,
    Subscription, Tag,
    Favourite, Ingredient
)
from .serializers import (
    FavouriteSerializer, PostRecipeSerializer,
    GetRecipeSerializer, IngredientSerializer,
    TagSerializer, RecipeToRepresentFavouriteSerializer,
    GetSubscribeSerializer, SubscribeSerializer,
    ShoppingListSerializer
)
from .permissions import IsAuthorOrReadOnly
from .filters import RecipeFilter, SearchFilter


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_class = [AllowAny]
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['name', ]


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_class = [AllowAny]
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer = PostRecipeSerializer
    permission_class = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetRecipeSerializer
        return PostRecipeSerializer


@api_view(['GET'])
def subscription_view(request):
    subscription_list = User.objects.filter(subcriptors__user=request.user)
    paginator = PageNumberPagination()
    paginator.page_size = 6
    result_page = paginator.paginate_queryset(subscription_list, request)
    serializer = GetSubscribeSerializer(result_page,
                                        many=True,
                                        context={'request': request})
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'DELETE'])
def subscription(request, id):
    user_to_subscribe = get_object_or_404(User, id=id)
    user = request.user
    subscribed = (
        Subscription.objects.filter(user=user,
                                    author=user_to_subscribe).exists()
    )
    if request.method == 'GET':
        data = {'user': request.user.id,
                'author': id}
        serializer = SubscribeSerializer(data=data,
                                         context={'request': request})
        if serializer.is_valid():
            serializer.save()
            sub_serializer = GetSubscribeSerializer(user_to_subscribe)
            return Response(sub_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        if not subscribed:
            return Response("Нет такой подписки", 
                            status=status.HTTP_400_BAD_REQUEST)
        obj = (
            Subscription.objects.filter(user=request.user,
                                        author=user_to_subscribe)
        )
        obj.delete()
        return Response('Автор удален из подписок', status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
def favourite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favourited = Favourite.objects.filter(recipe=recipe,
                                          user=request.user).exists()
    if request.method == 'GET':
        data = {
            'user': request.user.id,
            'recipe': recipe_id,
        }
        serializer = FavouriteSerializer(data=data,
                                         context={'request': request})
        if serializer.is_valid():
            serializer.save()
            recipe_serializer = (
                RecipeToRepresentFavouriteSerializer(recipe)
            )
            return Response(recipe_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if not favourited:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj = Favourite.objects.filter(recipe=recipe, user=request.user)
        obj.delete()
        return Response('Рецепт удален из избранного',
                        status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
def shoppinglist(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    is_in_list = Shoppinglist.objects.filter(recipe=recipe,
                                             user=request.user).exists()
    if request.method == 'GET':
        data = {
            'user': request.user.id,
            'recipe': id,
        }
        serializer = ShoppingListSerializer(data=data,
                                            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            recipe_serializer = RecipeToRepresentFavouriteSerializer(recipe)
            return Response(recipe_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        if not is_in_list:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj = Shoppinglist.objects.filter(recipe=recipe, user=request.user)
        obj.delete()
        return Response('Рецепт удален из списка покупок',
                        status.HTTP_204_NO_CONTENT)
