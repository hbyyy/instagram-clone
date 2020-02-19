from rest_framework import serializers

from members.serialrizers import UserSerializer
from .models import Post, PostImage


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


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'content',
        )

    def to_representation(self, instance):
        return PostSerializer(instance).data


# 숙제 풀
class PostImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = (
            'image',
        )
