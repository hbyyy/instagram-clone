from rest_framework import serializers

from members.serialrizers import UserSerializer
from .models import Post, PostImage, PostComment


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'content',
            'created',
            'postimage_set',
        )


# 숙제 해본
# class PostImageCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PostImage
#         fields = (
#             'image',
#         )

# 이미지를 같이 받을 수 있도
class PostCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField()
    )

    class Meta:
        model = Post
        fields = (
            'images',
            'content',
        )

    def to_representation(self, instance):
        return PostSerializer(instance).data

    # post는 따로 만들고, 이미지로 순회하면서 따로 저장
    def create(self, validated_data):
        images = validated_data.pop('images')
        post = super().create(validated_data)
        for image in images:
            serializer = PostImageCreateSerializer(data={'image': image})
            if serializer.is_valid():
                serializer.save(post=post)
        return post


# 숙제 풀이
class PostImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = (
            'image',
        )


class PostCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = PostComment
        fields = (
            'author',
            'pk',
            'content',
        )


class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = (
            'content',
        )

    def to_representation(self, instance):
        return PostCommentSerializer(instance).data
