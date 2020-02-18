from rest_framework import serializers

from members.serialrizers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'content',
            'created'
        )


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'content',
        )

    def to_representation(self, instance):
        return PostSerializer(instance).data
