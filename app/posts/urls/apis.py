from django.urls import path

from .. import apis

urlpatterns = [
    path('', apis.PostListCreateAPIView.as_view()),
    path('<int:pk>/images/', apis.PostImageCreateAPIView.as_view())
]