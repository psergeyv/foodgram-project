from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Seo, Textblock
from recipes.models import Recipes, Ingredient, IngredientRecipes, Tags



def index(request):      
    tags_filters = []
    if request.GET.get('f'):
        tags_filters = request.GET.get('f').split(',')
    
    seo_list = {"title":"","keywords":"", "description":""}
    seo = Seo.objects.filter(slug='index').first()
    if seo:
        seo_list = {"title": seo.title,
                    "keywords": seo.keywords,
                    "description":seo.description
                   }
    
    if len(tags_filters) > 0:
        recipes_list =  Recipes.objects.filter(tags__slug__in=tags_filters).order_by("-pub_date").distinct()
    else:
        recipes_list =  Recipes.objects.order_by("-pub_date").all() 

    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page_recipes = paginator.get_page(page_number)

    return render(request, "home.html", {
        "seo":seo_list,
        "recipes":page_recipes,
        "paginator":paginator,
    })
