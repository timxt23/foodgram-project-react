from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters

from .models import Ingredient, Recipe

User = get_user_model()


class IngredientFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)


class TagRecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='filter_is_favorite')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_is_favorite(self, queryset, name, value):
        user = self.request.user
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not self.request.user.is_anonymous:
            return queryset.filter(shopping_cart__user=user)
        return queryset