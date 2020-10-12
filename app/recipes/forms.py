from django import forms
from django.forms import ModelForm

from .models import Recipes


class RecipeCreateForm(ModelForm):

    class Meta:
        model = Recipes
        fields = ('title', 'tags', "cooking_time", "description", "image",)
       


class RecipeForm(ModelForm):

    class Meta:
        model = Recipes
        fields = ('title', "cooking_time", "description", "image",)
