from django import forms
from django.forms import ModelForm

from .models import Recipes


class RecipeCreateForm(ModelForm):

    class Meta:
        model = Recipes
        fields = ('title', 'tags', "cooking_time", "description", "image",)
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if title == '':
            raise forms.ValidationError(f'Название не может быть пустым!')
        return title  


class RecipeForm(ModelForm):

    class Meta:
        model = Recipes
        fields = ('title', "cooking_time", "description", "image",)

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if title == '':
            raise forms.ValidationError(f'Название не может быть пустым!')
        return title    
