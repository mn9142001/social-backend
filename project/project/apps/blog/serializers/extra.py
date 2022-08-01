from ..models import SnippetFile, Post
from rest_framework import serializers
from user.serializers import SnippetAuthorSerializer

class SnippetFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnippetFile
        fields = ('id', 'media',)


class BaseSnippetSerializer(serializers.ModelSerializer):
    author = SnippetAuthorSerializer(default=serializers.CurrentUserDefault())
    media = SnippetFileSerializer(many=True, required=False)

    class Meta:
        fields = ('id', 'author', 'date', 'content', 'media',)
        abstract = True


