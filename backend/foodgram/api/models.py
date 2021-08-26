from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey

from users.models import User 

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, 
                                   related_name='subscriptions')
    author = models.ForeignKey(User, on_delete=CASCADE, 
                                     related_name='subcriptors')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscription'
            )
        ]

class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    measurement_unit = models.CharField(max_length=15, 
                                        verbose_name='Единицы измерения')

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, 
                                                         verbose_name='Тег')
    color = models.CharField(max_length=7, 
                                default="#49B64E", 
                                unique=True,
                                blank=False, 
                                verbose_name='Цвет')
    slug = models.SlugField(max_length=200, unique=True, blank=False, 
                                                         verbose_name='Slug')

class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name='recipes', 
                                       verbose_name='Теги')
    author = models.ForeignKey(User, 
                        on_delete=models.CASCADE, 
                        related_name='recipes',
                        blank=False,
                        verbose_name='Автор')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', 
                                                    related_name='recipes', 
                                                    verbose_name='Ингредиенты')
    name = models.CharField(max_length=200,
                            blank=False, verbose_name='Название рецепта')
    image = models.ImageField(upload_to='app/',
                              blank=False, 
                              verbose_name='Изображение')
    cooking_time = models.PositiveIntegerField('Время приготовления')
    text = models.TextField(max_length=500)


    def __str__(self):
        return self.name 

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE, 
                                       related_name='ingredients_in')
    ingredient = models.ForeignKey(Ingredient, related_name='ingredients_in', 
                                               on_delete=CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0)])

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, 
                                   related_name='favourite')
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE, 
                                       related_name='in_favourite')

    class Meta:
        constraints = (models.UniqueConstraint(fields=['user', 'recipe'], 
                                               name='following_unique'),)

class Shoppinglist(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE, 
                                       related_name='recipes_in')
    user = models.ForeignKey(User, on_delete=CASCADE, 
                                   related_name='current_user')