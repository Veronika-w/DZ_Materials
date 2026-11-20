from django.urls import include, path

urlpatterns = [
    path("materials/", include("materials.urls", namespace="materials")),
    path("users/", include("users.urls")),
]
