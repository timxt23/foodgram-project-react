from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag
)


class RecipeIngredientsInLine(admin.TabularInline):
    model = Recipe.ingredient.through
    extra = 1


class RecipeTagsInLine(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientsInLine, RecipeTagsInLine)

    def count_favorites(self, obj):
        return obj.favorites.count()


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ['name']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
