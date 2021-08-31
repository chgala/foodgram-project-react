# from django.core import validators
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


from .models import (
            Recipe, Subscription, RecipeIngredient,
            Tag, Favourite, Ingredient, Shoppinglist
)
from users.models import User


def validate_author(data):
    if data.get('author') == data.get('user'):
        raise ValidationError('Нельзя подписаться на самого себя')
    return data


def get_existance(self, obj, model):
    request = self.context.get('request')
    if request is None or request.user.is_anonymous:
        return False
    return model.objects.filter(user=request.user, recipe=obj).exists()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return (
            Subscription.objects.filter(user=request.user, author=obj).exists()
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = ('author', 'user')
        validators = (validate_author, )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class GetRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = (
        serializers.CharField(read_only=True,
                              source='ingredient.measurement_unit')
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class PostRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(),
                                            source='ingredient.id')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class GetRecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    ingredients = GetRecipeIngredientSerializer(many=True,
                                                read_only=True,
                                                source='ingredients_in')
    author = UserSerializer()
    tags = TagSerializer(many=True)
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        return get_existance(self, obj, Favourite)

    def get_is_in_shopping_cart(self, obj):
        return get_existance(self, obj, Shoppinglist)


class PostRecipeSerializer(serializers.ModelSerializer):
    ingredients = PostRecipeIngredientSerializer(many=True,
                                                 source='ingredients_in')
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients_in')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            current_ingredient = (
                Ingredient.objects.get(pk=ingredient['ingredient']['id'].id)
            )
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):

        if 'ingredients' in self.initial_data:
            ingredients = validated_data.pop('ingredients_in')
            instance.ingredients.clear()
            for ingredient in ingredients:
                current_ingredient = (
                    get_object_or_404(Ingredient,
                                      pk=ingredient['ingredient']['id'].id)
                )
                if (
                    RecipeIngredient.objects.filter(
                        recipe=instance,
                        ingredient=current_ingredient).exists()
                ):
                    instance.ingredient.amount = (
                        ingredient['ingredient']['amount']
                    )
                else:
                    RecipeIngredient.objects.update_or_create(
                        recipe=instance,
                        ingredient=current_ingredient,
                        amount=ingredient['amount']
                    )
        if 'tags' in self.initial_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)

        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        instance.save()
        return instance


class RecipeSubscribe(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):

    def validate(self, data):
        id = data['author'].id
        user = data['user']
        if Subscription.objects.filter(author=id, user=user).exists():
            raise serializers.ValidationError('You are subscribed already!')
        return data

    class Meta:
        model = Subscription
        fields = '__all__'


class GetSubscribeSerializer(serializers.ModelSerializer):
    recipes = RecipeSubscribe(read_only=True, many=True)
    recipes_count = serializers.SerializerMethodField() 
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 
                  'first_name', 'last_name', 
                  'is_subscribed', 'recipes', 
                  'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return (
            Subscription.objects.filter(user=request.user, author=obj).exists()
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class RecipeToRepresentFavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavouriteSerializer(serializers.ModelSerializer):

    def validate(self, data):
        recipe_id = data['recipe'].id
        user = data['user']
        if Favourite.objects.filter(recipe=recipe_id, user=user).exists():
            raise serializers.ValidationError('You have already subscribed!')
        return data

    class Meta:
        model = Favourite
        fields = '__all__'


class ShoppingListSerializer(serializers.ModelSerializer):

    def validate(self, data):
        id = data['recipe'].id
        user = data['user']
        if Shoppinglist.objects.filter(recipe=id, user=user).exists():
            raise serializers.ValidationError(
                'This recipe is already in your shopping list!'
            )
        return data

    class Meta:
        model = Shoppinglist
        fields = '__all__'
