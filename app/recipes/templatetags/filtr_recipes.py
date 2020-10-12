from django import template
from actions.models import Follow, Favorites, ShoppingList
from recipes.models import Recipes

register = template.Library()


@register.filter(name='items_follow')
def get_filter_values(request, author_id):
    return Recipes.objects.filter(author=author_id).order_by("pub_date")[:3]


@register.filter(name='count_recipises')
def get_filter_values(request, author_id):
    count = Recipes.objects.filter(author=author_id).count()
    return (count - 3)


@register.filter(name='in_favorites')
def get_filter_values(request, recipe_id):
    is_favorite = Favorites.objects.filter(
        recipe_id=recipe_id).filter(fuser=request.user).all()
    return is_favorite.count()


@register.filter(name='count_shoplist')
def get_filter_values(request):
    counts_list = ShoppingList.objects.filter(user=request.user).all()
    return counts_list.count()


@register.filter(name='is_shoplist')
def get_filter_values(request, recipe_id):
    is_slist = ShoppingList.objects.filter(user=request.user).filter(
        recipe_id=recipe_id).all()
    if is_slist:   
        return True
    return False    
