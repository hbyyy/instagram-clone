from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.serializers import PostSerializer, PostCreateSerializer, PostImageCreateSerializer, PostCommentSerializer, \
    PostCommentCreateSerializer
from .models import Post, PostComment


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


# 숙제 해본것
# class PostImageCreateAPIView(APIView):
#     def post(self, request, pk):
#         # 여러장의 이미지를 받아서
#         # 특정 Post에 연결되는 PostImage를 생성
#         # /posts/1/images
#         result = []
#         for image in request.data.getlist('image'):
#             serializer = PostImageCreateSerializer(data={'image': image})
#             if serializer.is_valid():
#                 serializer.save(post=Post.objects.get(pk=pk))
#                 result.append(serializer.data)
#             else:
#                 return Response(serializer.errors)
#         return Response(result)

# 숙제 풀이
class PostImageCreateAPIView(APIView):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        for image in request.data.getlist('image'):
            serializer = PostImageCreateSerializer(data={'image': image})
            if serializer.is_valid():
                serializer.save(post=post)

        serializer = PostSerializer(post)
        return Response(serializer.data)


# class PostCommentListCreateAPIView(APIView):
#     def get(self, request, post_pk):
#         comments = PostComment.objects.filter(post__pk=post_pk)
#         serializer = PostCommentSerializer(comments, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, post_pk):
#         serializer = PostCommentCreateSerializer(data=request.data)
#         post = get_object_or_404(Post, pk=post_pk)
#         if serializer.is_valid():
#             serializer.save(post=post, author=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator()
class PostCommentListCreateView(generics.ListCreateAPIView):

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        return PostComment.objects.filter(post=post_pk)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostCommentSerializer
        elif self.request.method == 'POST':
            return PostCommentCreateSerializer

    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        serializer.save(post=post, author=self.request.user)
