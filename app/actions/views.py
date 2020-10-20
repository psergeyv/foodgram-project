import json
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from django.contrib.auth.decorators import login_required
from recipes.models import Recipes, Ingredient, IngredientRecipes
from .models import Follow, Favorites, ShoppingList
from users.models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def add_favorite(request):
    if request.method == "POST":
        recipe_id = int(json.loads(request.body).get('id'))
        created = Favorites.objects.get_or_create(
            fuser_id=request.user.id, recipe_id=recipe_id)
        if not created:
            return JsonResponse({'success': False})

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def delete_favorite(request, recipe_id):
    if request.method == "DELETE":
        user = request.user
        deleted = Favorites.objects.filter(
            fuser_id=user.id, recipe_id=recipe_id).delete()
        return JsonResponse({'success': True}) if deleted else JsonResponse({'success': False})
    else:
        return JsonResponse({'success': False})


@login_required
def add_subscription(request):
    following_id = int(json.loads(request.body).get('id'))
    if request.user.id != following_id:
        created = Follow.objects.get_or_create(
            user_id=request.user.id, author_id=following_id)
    return JsonResponse({'success': True}) if created else JsonResponse({'success': False})


@login_required
def delete_subscription(request, following_id):
    deleted = Follow.objects.filter(
        user_id=request.user.id, author_id=following_id).delete()
    return JsonResponse({'success': True}) if deleted else JsonResponse({'success': False})


def get_ingredients(request):
    query = str(request.GET.get("query")).lower()
    ingredients = Ingredient.objects.filter(
        title__contains=query).values("title", "dimension")
    return JsonResponse(list(ingredients), safe=False)


def add_purchases(request):
    if request.method == "POST":
        recipe_id = int(json.loads(request.body).get('id'))
        created = ShoppingList.objects.get_or_create(
            user_id=request.user.id, recipe_id=recipe_id)
        if not created:
            return JsonResponse({'success': False})

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def delete_purchases(request, recipe_id):
    if request.method == "DELETE":
        deleted = ShoppingList.objects.filter(
            user_id=request.user.id, recipe_id=recipe_id).delete()
        return JsonResponse({'success': True}) if deleted else JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


@login_required
def dwl_purchases(request):
    shop_list = ShoppingList.objects.filter(
        user_id=request.user.id).values_list("recipe", flat=True).all()
    ingredientList = IngredientRecipes.objects.filter(
        recipe_id__in=shop_list).order_by('ingredient')
    
    outList = {}
    for value in ingredientList:
        if not value.ingredient in outList.keys():
            outList[value.ingredient] = value.count
        else:
            outList[value.ingredient] += value.count
            

    myshoplist = []
    myshoplist.append('Список покупок:')
    myshoplist.append('\n\n')
    for key, val in outList.items():
        myshoplist.append(f'{key.title} - {val} {key.dimension} \n')
    myshoplist.append('\n\n')
    myshoplist.append('* * *')
    myshoplist.append('\n')
    myshoplist.append('Приятного аппетита!')
    #при желании можно сделать вывод в PDF или как угодно

    response = HttpResponse(myshoplist, 'Content-Type: text/plain')
    response['Content-Disposition'] = 'attachment; filename="myshoplist.txt"'
    return response
