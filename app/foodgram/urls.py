
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500

handler404 = "actions.views.page_not_found"
handler500 = "actions.views.server_error"

urlpatterns = [
    path("", include("home.urls")), 
    path("", include("actions.urls")),   
    path("recipes/", include("recipes.urls")),
    path('admin/', admin.site.urls),
    path("accounts/", include("users.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += [
        path('about/', views.flatpage, {'url': '/about/'}, name='author'),
        path('technology/', views.flatpage, {'url': '/technology/'}, name='technology'),
]

if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)