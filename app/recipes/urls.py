
from django.urls import path
from . import views

urlpatterns = [
    path("favorites/", views.favorites, name="favorites"),
    path("follow/", views.followes, name="follow"),
    path("subscribe/", views.favorites, name="subscribe"),
    path("purchases/", views.purchases, name="purchases"),

    path("new/", views.user_recipe_new, name="recipe_new"),
    path("edit/<int:id>/", views.user_recipe_edit, name="recipe_edit" ),
    path("delete/<int:id>/", views.delete_recipe,name="recipe_delete"),
    path("<int:user_id>/", views.list_user_recipes, name="list_recipes_author"),
    path("<int:user_id>/<int:id>/", views.view_user_recipes, name="view_recipe"),
]
