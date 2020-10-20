from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.edit_profile, name="edit_profile"),
    path('signup/', views.SignUp.as_view(), name='signup'),    
]
