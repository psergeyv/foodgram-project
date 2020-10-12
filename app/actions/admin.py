from django.contrib import admin
from .models import Favorites,Follow,ShoppingList

@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'fuser', )
    search_fields = ('fuser', )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', )
    search_fields = ('user', )    

@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe',)        