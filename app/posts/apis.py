from rest_framework.response import Response
from rest_framework.views import APIView

from posts.serializers import PostSerializer
from .models import Post


class PostListCreateAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
