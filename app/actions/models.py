from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipes

User = get_user_model()


class Follow(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower", verbose_name="Подписчик")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following", verbose_name="Автор постов")


class Favorites(models.Model):    
    fuser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites_user", verbose_name="Пользователь")
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name="favorite_recipe", verbose_name="Рецепт в избранном")


class ShoppingList(models.Model):    
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shoplist_user", verbose_name="Пользователь")
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name="shoplist_recipe", verbose_name="Рецепт с продуктами для покупки")
