from django.urls import path

from . import views


urlpatterns = [
    path("ingredients/", views.get_ingredients, name="get_ingredients"),
    path("favorites", views.add_favorite, name="add_favorite"),
    path("favorites/", views.add_favorite, name="add_favorite"),
    path("favorites/<int:recipe_id>",
         views.delete_favorite, name="delete_favorite"),
    path("purchases", views.add_purchases, name="add_purchases"),
    path("purchases/", views.add_purchases, name="add_purchases"),
    path("purchases/<int:recipe_id>",
         views.delete_purchases, name="delete_purchases"),
    path("purchases/<int:recipe_id>/",
         views.delete_purchases, name="delete_purchases"),
    path("subscriptions", views.add_subscription, name="add_subscription"),
    path("subscriptions/", views.add_subscription, name="add_subscription"),
    path("subscriptions/<int:following_id>",
         views.delete_subscription, name="delete_subscription"),
    
    path("dwl_purchases/", views.dwl_purchases, name="dwl_purchases"),
]
