from django.contrib import admin
from django.db.models import Count

from .models import Ingredient, IngredientRecipes, Recipes, Tags


class IngredientRecipesInline(admin.TabularInline):
    model = IngredientRecipes
    verbose_name = 'Ингредиент'


class RecipesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"urlcode": ("title",)}
    inlines = (IngredientRecipesInline,)
    list_display = (
        'image_img', 'title', 'author', 
        'cooking_time', 'id', 
    )
    list_display_links = ('title', 'image_img')
    list_filter = ('author', )
    search_fields = ('title', 'author__username', )
    autocomplete_fields = ('author', )
    ordering = ('-pub_date', )
   


admin.site.register(Recipes, RecipesAdmin)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'dimension', )
    search_fields = ('^title', )


@admin.register(IngredientRecipes)
class IngredientRecipesAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'count', )
    list_display_links = ('ingredient',)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'slug')
    list_display_links = ('title', 'slug')