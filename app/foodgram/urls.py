
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("home.urls")),
    path("recipes/", include("recipes.urls")),
    path('admin/', admin.site.urls),
    path("accounts/", include("users.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

#handler404 = "recipes.views.page_not_found"
#handler500 = "recipes.views.server_error"

if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)