"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from members.views import signup_view
from posts.views import post_list

# drf-yasg 사용
schema_view = get_schema_view(
    openapi.Info(
        title='WPS Instagram API',
        default_version='v1',
        contact=openapi.Contact(email='qjaduddl94@gmail.com'),
    ),
    public=True,
)

urlpatterns_apis = [
    path('members/', include('members.urls.apis')),
    path('posts/', include('posts.urls.apis'))
]

urlpatterns = [
    path('doc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('apis/', include(urlpatterns_apis)),
    path('admin/', admin.site.urls),
    path('members/', include('members.urls.views')),
    path('posts/', include('posts.urls.views')),
    path('', signup_view, name='signup'),
    path('explore/tags/<str:tag>/', post_list, name='post-list-tag'),
]

urlpatterns += static(
    # URL 앞부분이 /media/이면
    prefix=settings.MEDIA_URL,
    # document_root 위치에서 나머지 path에 해당하는 파일을 리턴
    document_root=settings.MEDIA_ROOT,
)
