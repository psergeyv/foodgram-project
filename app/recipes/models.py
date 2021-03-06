import sys
from io import BytesIO

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from PIL import Image
from sorl.thumbnail import ImageField, get_thumbnail

User = get_user_model()


def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.user.id, filename)


class Tags(models.Model):

    title = models.CharField('Название', max_length=10, null=False, default="")
    style = models.CharField('Стиль', max_length=30,
                             null=False, default="green")
    slug = models.SlugField(max_length=15, unique=True, default="",
                            null=False, verbose_name="Код")

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    dimension = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} ({self.dimension})"

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_author',
        verbose_name='Автор',
    )
    name = models.CharField('Название', max_length=200, blank=False)
    image = models.ImageField(
        upload_to='irecipes/%d_%m_%Y/',
        verbose_name='Картинка',
    )
    description = RichTextUploadingField('Текстовое описание', blank=False)
    ingredient = models.ManyToManyField(
        'Ingredient',
        related_name='recipe_ingredient',
        through='IngredientRecipes',
        verbose_name='Ингредиент',
    )

    tags = models.ManyToManyField(
        Tags,
        related_name='recipes_tags',
        verbose_name='ТЭГ')
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')

    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    urlcode = models.SlugField(max_length=100, unique=True, default=None,
                               null=True, verbose_name="Символьный код")

    class Meta:
        ordering = ('-pub_date', 'name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Recipes, self).delete(*args, **kwargs)
        storage.delete(path)


class IngredientRecipes(models.Model):
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name='recipe_count', verbose_name="Рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients', verbose_name="Ингредиент"
    )
    count = models.IntegerField(verbose_name="Количество")

    def __str__(self):
        return self.ingredient.title

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'
