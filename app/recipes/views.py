from actions.models import Favorites, Follow, ShoppingList
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from home.models import Seo, Textblock

from .forms import RecipeCreateForm, RecipeForm
from .models import Ingredient, IngredientRecipes, Recipes, Tags
from .utils import get_ingredients, get_tags_for_edit

User = get_user_model()


def list_user_recipes(request, user_id):

    seo_list = {"title": "", "keywords": "", "description": ""}
    seo = Seo.objects.filter(slug='index').first()
    if seo:
        seo_list = {"title": seo.title,
                    "keywords": seo.keywords,
                    "description": seo.description
                    }

    author = get_object_or_404(User, id=user_id)
    list_tags = Tags.objects.order_by('title').all()
    tags = {}

    tags_filters = []
    if request.GET.get('f'):
        tags_filters = request.GET.get('f').split(',')

    if len(tags_filters) > 0:
        recipes_list = Recipes.objects.filter(author=author.id).filter(
            tags__slug__in=tags_filters).order_by("pub_date").distinct()
    else:
        recipes_list = Recipes.objects.filter(
            author=author.id).order_by("pub_date").distinct()

    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page_recipes = paginator.get_page(page_number)

    return render(request, "authorRecipe.html", {
        "seo": seo_list,
        "recipes": page_recipes,
        'author': author,
        "paginator": paginator
    })


def view_user_recipes(request, user_id, id):

    recipe = get_object_or_404(Recipes, id=id)
    ingedients = IngredientRecipes.objects.filter(recipe=recipe).all()

    is_favorite = 0
    is_following = 0
    is_purchases = 0

    if request.user.is_authenticated:
        is_favorite = Favorites.objects.filter(
            recipe=recipe).filter(fuser=request.user).count
        is_following = Follow.objects.filter(
            author=user_id).filter(user=request.user).count
        is_purchases = ShoppingList.objects.filter(
            recipe=recipe).filter(user=request.user).count

    return render(request, "item/singlePage.html", {
        "recipe": recipe,
        "ingedients": ingedients,
        'is_favorite': is_favorite,
        'is_following': is_following,
        'is_purchases': is_purchases,
    })


@login_required
def user_recipe_new(request):
    head_form = 'Создание рецепта'
    text_btn_form = 'Создать рецепт'
    form = RecipeCreateForm(
        request.POST or None,
        files=request.FILES or None
    )

    if request.method == "POST" and form.is_valid():
        newRecipe = form.save(commit=False)
        newRecipe.author = request.user
        newRecipe.save()

        ingredient_temp = []
        for fing in request.POST:
            t = fing.split('_')
            if 'nameIngredient' == t[0]:
                ingredient_temp.append(request.POST[f'nameIngredient_{t[1]}'])

                if request.POST[f'valueIngredient_{t[1]}'] == '':
                    count = 0
                else:
                    count = int(request.POST[f'valueIngredient_{t[1]}'])
                ingredient = Ingredient.objects.get(
                    title=request.POST[f'nameIngredient_{t[1]}'])
                IngredientsAdd = IngredientRecipes.objects.create(
                    recipe=newRecipe,
                    ingredient=ingredient,
                    count=count
                )
                IngredientsAdd.save()
        form.save_m2m()
        return redirect(
            'view_recipe',
            user_id=request.user.id,
            id=newRecipe.id
        )

    tags = Tags.objects.all()
    return render(request, "formRecipe.html", {
        'form': form,
        'head_form': head_form,
        'tags': tags,
        'text_btn_form': text_btn_form
    })


@login_required
def user_recipe_edit(request, id):
    recipe = get_object_or_404(Recipes, id=id)

    if recipe.author != request.user:
        return redirect('view_recipe', recipe.author.id, id)
    head_form = f'Редактирование рецепта ({recipe.name})'
    text_btn_form = 'Сохранить изменения'
    form = RecipeCreateForm(request.POST or None,
                            files=request.FILES or None, instance=recipe)

    if request.method == "POST":

        if form.is_valid():
            form.save()
            IngredientRecipes.objects.filter(recipe=recipe).delete()

            ingredient_temp = []
            for fing in request.POST:
                t = fing.split('_')
                if 'nameIngredient' == t[0]:
                    ingredient_temp.append(
                        request.POST[f'nameIngredient_{t[1]}'])

                    if request.POST[f'valueIngredient_{t[1]}'] == '':
                        count = 0
                    else:
                        count = int(request.POST[f'valueIngredient_{t[1]}'])
                    ingredient = Ingredient.objects.get(
                        title=request.POST[f'nameIngredient_{t[1]}'])
                    IngredientsAdd = IngredientRecipes.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        count=count
                    )
                    IngredientsAdd.save()

            return redirect('view_recipe', user_id=request.user.id, id=recipe.id)

    tags = Tags.objects.all()
    list_tags = recipe.tags.values_list('slug', flat=True)
    list_ingredients = IngredientRecipes.objects.filter(recipe=recipe.id)

    return render(request, "formRecipe.html", {
        'form': form,
        'head_form': head_form,
        'recipe': recipe,
        'tags': tags,
        'list_tags': list_tags,
        'list_ingredients': list_ingredients,
        'text_btn_form': text_btn_form,
    })


@login_required
def favorites(request):
    seo_list = {"title": "Избранное",
                "keywords": "Избранное", "description": "Избранное"}
    seo = Seo.objects.filter(slug='favorites').first()
    if seo:
        seo_list = {"title": seo.title,
                    "keywords": seo.keywords,
                    "description": seo.description
                    }
    hrmlBlock = Textblock.objects.filter(pageblock='index').all()
    hrmlBl = {}
    for tb in hrmlBlock:
        hrmlBl[tb.codeblock] = {'name': tb.name, 'description': tb.description}

    tags_filters = []
    if request.GET.get('f'):
        tags_filters = request.GET.get('f').split(',')

    if len(tags_filters) > 0:
        recipes = Recipes.objects.filter(
            favorite_recipe__fuser=request.user).filter(
            tags__slug__in=tags_filters).order_by("pub_date").all()
    else:
        recipes = Recipes.objects.filter(
            favorite_recipe__fuser=request.user).order_by("pub_date").all()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'favorites.html', context)


@login_required
def followes(request):

    myFollow = Follow.objects.filter(
        user_id=request.user.id).order_by("author").all()

    paginator = Paginator(myFollow, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'follow.html', context)


def purchases(request):
    ShopList = ShoppingList.objects.filter(
        user_id=request.user.id).all()
    ShopListCount = ShoppingList.objects.filter(
        user_id=request.user.id).count

    context = {
        'ShopList': ShopList,
        'ShopListCount': ShopListCount
    }
    return render(request, 'shopList.html', context)


@login_required
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipes, id=id)
    if request.user == recipe.author:
        Recipes.objects.filter(id=id).delete()
        return redirect("list_recipes_author", request.user.id)
    return redirect("list_recipes_author", request.user.id)
