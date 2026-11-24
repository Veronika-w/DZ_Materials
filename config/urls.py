from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path("materials/", include("materials.urls", namespace="materials")),
    path("users/", include("users.urls", namespace="users")),
]
