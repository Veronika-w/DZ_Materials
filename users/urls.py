from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig

from .views import (PaymentsViewSet, UserCreateAPIView,
                    UserRetrieveUpdateAPIView)

app_name = UsersConfig.name

router = DefaultRouter()
router.register("payments", PaymentsViewSet, basename="payments")

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("me/", UserRetrieveUpdateAPIView.as_view(), name="profile"),
    path("", include(router.urls)),
    path("login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path("token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]