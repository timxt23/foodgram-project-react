from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, validators

from users.models import Subscription
from users.serializers import CustomUserSerializer
from .models import Ingredient, IngredientRecipe, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор обработки ингредиентов"""
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор обработки тэгов"""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=IngredientRecipe.objects.all(),
                fields=['recipe', 'ingredient']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    """Class for converting recipe data."""
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        recipe = obj
        return recipe.ingredient.annotate(
            amount=F('ingredientrecipe__amount'),
        ).values(
            'id',
            'name',
            'measurement_unit',
            'amount'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            shopping_cart__user=user,
            id=obj.id
        ).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredient,
                id=ingredient_item['id']
            )
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Необходимы уникальные ингредиенты'
                )
        data['ingredients'] = ingredients
        return data

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            amount = ingredient.get('amount')
            if int(amount) < 1:
                raise serializers.ValidationError(
                    'Кол-во должно быть больше 1'
                )
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=amount,
            )

    @transaction.atomic
    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')
            instance.ingredient.clear()
            self.create_ingredients(ingredients_data, instance)
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        return super().update(instance, validated_data)


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'image', 'name', 'cooking_time')
        read_only_fields = ('id', 'image', 'name', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_following = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_following',
            'recipes_count',
            'recipes'
        )

    def get_is_following(self, obj):
        return Subscription.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return ShortRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
