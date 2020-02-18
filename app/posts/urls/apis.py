from django.urls import path

from .. import apis

urlpatterns = [
    path('', apis.PostListCreateAPIView.as_view())
]