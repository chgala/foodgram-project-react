from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter as BaseSearchFilter

from .models import Recipe, Tag

class RecipeFilter(filters.FilterSet):
    is_favourited = filters.BooleanFilter(method='get_is_favourited')
    is_in_shopping_cart = filters.BooleanFilter(method='get_is_in_shopping_cart')
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug', 
                                             to_field_name='slug', 
                                             queryset = Tag.objects.all())

    def get_is_favourited(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(in_favourite__user=self.request.user)
        return Recipe.objects.all()
 
    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(recipes_in__user=self.request.user)
        return Recipe.objects.all()

class SearchFilter(BaseSearchFilter):
    search_param = 'name'
