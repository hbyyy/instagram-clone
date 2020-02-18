from django.urls import path

from members import apis


urlpatterns = [
    path('auth-token/', apis.AuthTokenAPIView.as_view())
]