from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.serializers import PostSerializer, PostCreateSerializer, PostImageCreateSerializer
from .models import Post, PostImage


# class PostListCreateAPIView(APIView):
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         # form-data 방식으로 content, 복수의 image 를 받을 수 있도록 구현해보자
#         # post 를 생성한 후 한번에 받을 image 를 사용해서 post와 연결되는 postimage를 사용
#
#         serializer = PostCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.order_by('-pk')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        elif self.request.method == 'POST':
            return PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostImageCreateAPIView(APIView):
    def post(self, request, pk):
        # 여러장의 이미지를 받아서
        # 특정 Post에 연결되는 PostImage를 생성
        # /posts/1/images
        result = []
        for image in request.data.getlist('image'):
            serializer = PostImageCreateSerializer(data={'image': image})
            if serializer.is_valid():
                serializer.save(post=Post.objects.get(pk=pk))
                result.append(serializer.data)
            else:
                return Response(serializer.errors)
        return Response(result)



        # images = request.data.getlist('image')
        # post = Post.objects.get(pk=pk)
        # for image in images:
        #     PostImage.objects.create(post=post, image=image)
        #
        # serializer = PostSerializer(post)
        # return Response(serializer.data)
