from django.contrib import admin

from .models import Ingredient, Tag, Recipe

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'author', 'get_favourite_count')
    search_fields = ('name', 'author', 'tags__name')

    @staticmethod
    def get_favourite_count(obj):
        return obj.in_favourite.count()


admin.site.register(Ingredient, IngredientAdmin) 
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin) 
