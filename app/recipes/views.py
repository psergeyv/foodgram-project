from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator

from home.models import Seo, Textblock
from .models import Recipes, Ingredient, IngredientRecipes, Tags

from django.contrib.auth import get_user_model
User = get_user_model()

def list_user_recipes(request,user_id):    
    seo_list = {"title":"","keywords":"", "description":""}
    seo = Seo.objects.filter(slug='index').first()
    if seo:
        seo_list = {"title": seo.title,
                    "keywords": seo.keywords,
                    "description":seo.description
                   }
    hrmlBlock = Textblock.objects.filter(pageblock='index').all()
    hrmlBl = {}
    for tb in hrmlBlock:
        hrmlBl[tb.codeblock] = {'name': tb.name,'description': tb.description}

    author = get_object_or_404(User, id=user_id)    

    recipes_list =  Recipes.objects.filter(author=author.id).order_by("pub_date").all()     
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page_recipes = paginator.get_page(page_number)

    

    return render(request, "authorRecipe.html", {
        "seo":seo_list,
        "hrmlBlock":hrmlBl,
        "recipes":page_recipes,
        'author':author,
    })


def view_user_recipes(request,user_id,id):    
    seo_list = {"title":"","keywords":"", "description":""}
    seo = Seo.objects.filter(slug='index').first()
    if seo:
        seo_list = {"title": seo.title,
                    "keywords": seo.keywords,
                    "description":seo.description
                   }
    hrmlBlock = Textblock.objects.filter(pageblock='index').all()
    hrmlBl = {}
    for tb in hrmlBlock:
        hrmlBl[tb.codeblock] = {'name': tb.name,'description': tb.description}

    
    recipe = get_object_or_404(Recipes, id=id) 
    return render(request, "item/singlePage.html", {
        "seo":seo_list,
        "hrmlBlock":hrmlBl,
        "recipe":recipe,
    })

def user_recipe_edit(request,user_id,id):    
    seo_list = {"title":"","keywords":"", "description":""}
    seo = Seo.objects.filter(slug='index').first()
    if seo:
        seo_list = {"title": seo.title,
                    "keywords": seo.keywords,
                    "description":seo.description
                   }
    hrmlBlock = Textblock.objects.filter(pageblock='index').all()
    hrmlBl = {}
    for tb in hrmlBlock:
        hrmlBl[tb.codeblock] = {'name': tb.name,'description': tb.description}

    recipes_list =  Recipes.objects.order_by("pub_date").all()     
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page_recipes = paginator.get_page(page_number)

    return render(request, "home.html", {
        "seo":seo_list,
        "hrmlBlock":hrmlBl,
        "recipes":page_recipes,
    })  

def user_recipe_delete(request,username,id):    
    seo_list = {"title":"","keywords":"", "description":""}
    seo = Seo.objects.filter(slug='index').first()
    if seo:
        seo_list = {"title": seo.title,
                    "keywords": seo.keywords,
                    "description":seo.description
                   }
    hrmlBlock = Textblock.objects.filter(pageblock='index').all()
    hrmlBl = {}
    for tb in hrmlBlock:
        hrmlBl[tb.codeblock] = {'name': tb.name,'description': tb.description}

    recipes_list =  Recipes.objects.order_by("pub_date").all()     
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page_recipes = paginator.get_page(page_number)

    return render(request, "home.html", {
        "seo":seo_list,
        "hrmlBlock":hrmlBl,
        "recipes":page_recipes,
    })        