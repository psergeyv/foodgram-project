
from django.urls import path
from . import views

urlpatterns = [
    path("favorites/", views.favorites, name="favorites"),
    path("follow/", views.followes, name="follow"),
    path("subscribe/", views.favorites, name="subscribe"),
    path("purchases/", views.purchases, name="purchases"),

    path("new/", views.user_recipe_new, name="unew"),
    path("edit/<int:id>/", views.user_recipe_edit, name="uedit" ),
    path("delete/<int:id>/", views.delete_recipe,name="udelete"),
    path("<int:user_id>/", views.list_user_recipes, name="urecipes"),
    path("<int:user_id>/<int:id>/", views.view_user_recipes, name="urecipe"),
]
