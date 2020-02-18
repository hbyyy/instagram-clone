from django.urls import path

from .. import apis


urlpatterns = [
    path('auth-token/', apis.AuthTokenAPIView.as_view())
]