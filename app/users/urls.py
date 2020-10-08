from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.EditProfile, name="EditProfile"),
    path('signup/', views.SignUp.as_view(), name='signup'),    
]
