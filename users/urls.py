from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaymentsViewSet, UserRetrieveUpdateAPIView

router = DefaultRouter()
router.register("payments", PaymentsViewSet, basename="payments")

urlpatterns = [
    path("me/", UserRetrieveUpdateAPIView.as_view(), name="profile"),
    path("", include(router.urls)),
]