
from django.urls import path
from . import views

urlpatterns = [
    path("<int:user_id>/", views.list_user_recipes, name="urecipes"),
    
    path("<int:user_id>/<int:id>", views.view_user_recipes, name="urecipe"),
    path(
        "<int:user_id>/<int:id>/edit",
        views.user_recipe_edit,
        name="uedit"
    ),
    path(
        "<int:user_id>/<int:id>/delete",
        views.user_recipe_delete,
        name="udelete"
    )
]


    