from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Seo, Textblock
from recipes.models import Recipes, Ingredient, IngredientRecipes, Tags



def index(request):  
    bdTags = Tags.objects.order_by("title").all()
    tags = {}
    tags_filters = []
    for tag in bdTags:
        tags[tag.slug] = {'title':tag.title,'style':tag.style}
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
            tags[tag.slug]['url'] = '/'  
    
    seo_list = {"title":"","keywords":"", "description":""}
    seo = Seo.objects.filter(slug='index').first()
    if seo:
        seo_list = {"title": seo.title,
                    "keywords": seo.keywords,
                    "description":seo.description
                   }
    
    if len(tags_filters) > 0:
        recipes_list =  Recipes.objects.filter(tags__id__in=tags_filters).order_by("pub_date").distinct()
    else:
        recipes_list =  Recipes.objects.order_by("pub_date").all() 

    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page_recipes = paginator.get_page(page_number)

    return render(request, "home.html", {
        "seo":seo_list,
        "recipes":page_recipes,
        "tags":tags,  
        "paginator":paginator,
    })
