from django.urls import path

from users.views import PaymentsViewSet

app_name = 'users'

urlpatterns = [
    path( "payments/<int:pk>/", PaymentsViewSet.as_view(), name="payments_list"),
]