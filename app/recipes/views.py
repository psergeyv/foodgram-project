from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from home.models import Seo, Textblock
from .models import Recipes, Ingredient, IngredientRecipes, Tags
from actions.models import Follow, Favorites, ShoppingList
from .forms import RecipeCreateForm, RecipeForm
from .utils import get_ingredients, get_tags_for_edit

User = get_user_model()


def list_user_recipes(request, user_id):
    bdTags = Tags.objects.order_by("title").all()
    tags = {}
    tags_filters = []
    for tag in bdTags:
        tags[tag.slug] = {'title': tag.title, 'style': tag.style}
        tempTags = []
        if request.GET.get('f'):
            tempTags = request.GET.get('f').split(',')
        if tag.slug in tempTags:
            tags_filters.append(tag.id)
            tags[tag.slug]['view'] = True
            tempTags.remove(tag.slug)
        else:
            tags[tag.slug]['view'] = False
            tempTags.append(tag.slug)
        if len(tempTags) > 0:
            tags[tag.slug]['url'] = '?f='+','.join(tempTags)
        else:
            tags[tag.slug]['url'] = '/recipes/'+str(user_id)

    seo_list = {"title": "", "keywords": "", "description": ""}
    seo = Seo.objects.filter(slug='index').first()
    if seo:
        seo_list = {"title": seo.title,
                    "keywords": seo.keywords,
                    "description": seo.description
                    }

    author = get_object_or_404(User, id=user_id)

    if len(tags_filters) > 0:
        recipes_list = Recipes.objects.filter(author=author.id).filter(
            tags__id__in=tags_filters).order_by("pub_date").distinct()
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
        "tags": tags,
        "paginator": paginator
    })


def view_user_recipes(request, user_id, id):
    seo_list = {"title": "", "keywords": "", "description": ""}
    seo = Seo.objects.filter(slug='index').first()
    if seo:
        seo_list = {"title": seo.title,
                    "keywords": seo.keywords,
                    "description": seo.description
                    }

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
        "seo": seo_list,
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

    if request.method == "POST":
        form = RecipeCreateForm(
            request.POST or None,
            files=request.FILES or None
        )

        if form.is_valid():

            newRecipe = form.save(commit=False)
            newRecipe.author = request.user
            newRecipe.save()

            ingTemp = []
            for fing in request.POST:
                t = fing.split('_')
                if 'nameIngredient' == t[0]:
                    ingTemp.append(request.POST[f'nameIngredient_{t[1]}'])

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

            return redirect(
                'urecipe',
                user_id=request.user.id,
                id=newRecipe.id
            )

    form = RecipeCreateForm()
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
        return redirect('urecipe', recipe.author.id, id)
    head_form = f'Редактирование рецепта ({recipe.title})'
    text_btn_form = 'Сохранить изменения'
    form = RecipeCreateForm(request.POST or None,
                            files=request.FILES or None, instance=recipe)

    if request.method == "POST":

        if form.is_valid():
            form.save()
            IngredientRecipes.objects.filter(recipe=recipe).delete()

            ingTemp = []
            for fing in request.POST:
                t = fing.split('_')
                if 'nameIngredient' == t[0]:
                    ingTemp.append(request.POST[f'nameIngredient_{t[1]}'])

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

            return redirect('urecipe', user_id=request.user.id, id=recipe.id)

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
    bdTags = Tags.objects.order_by("title").all()
    tags = {}
    tags_filters = []
    for tag in bdTags:
        tags[tag.slug] = {'title': tag.title, 'style': tag.style}
        tempTags = []
        if request.GET.get('f'):
            tempTags = request.GET.get('f').split(',')
        if tag.slug in tempTags:
            tags_filters.append(tag.id)
            tags[tag.slug]['view'] = True
            tempTags.remove(tag.slug)
        else:
            tags[tag.slug]['view'] = False
            tempTags.append(tag.slug)
        if len(tempTags) > 0:
            tags[tag.slug]['url'] = '?f='+','.join(tempTags)
        else:
            tags[tag.slug]['url'] = '/recipes/favorites/'

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
    if len(tags_filters) > 0:
        recipes = Recipes.objects.filter(
            favorite_recipe__fuser=request.user).filter(
            tags__id__in=tags_filters).order_by("pub_date").all()
    else:
        recipes = Recipes.objects.filter(
            favorite_recipe__fuser=request.user).order_by("pub_date").all()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags
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
        'tags': {},
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
        return redirect("urecipes", request.user.id)
    return redirect("urecipes", request.user.id)
