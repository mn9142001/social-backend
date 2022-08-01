from . import SnippetAuthorSerializer, serializers
from ..models import Post, SnippetFile
from .extra import SnippetFileSerializer
from .extra import BaseSnippetSerializer

class SharedPostSerializer(BaseSnippetSerializer):
    class Meta(BaseSnippetSerializer.Meta):
        model = Post
        fields = BaseSnippetSerializer.Meta.fields


class PostSerializer(serializers.ModelSerializer):
    media = SnippetFileSerializer(many=True, required=False)
    author = SnippetAuthorSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('content', 'author', 'media', 'post')

    def create(self, validated_data):
        self._creating = True
        _files = validated_data.get('media', [])
        if _files:
            media = SnippetFile.objects.bulk_create([SnippetFile(media=file) for file in _files])
            validated_data['media'] = media
        return Post.objects.create(**validated_data)
    
    def to_representation(self, instance : Post):
        data = super().to_representation(instance)
        if getattr(self, '_creating', False):
            #not fetching data from database 
            data['comments'] = 0
            data['shares'] = 0
            data['reacts'] = 0
        else:
            if instance.post:
                data['post'] = SharedPostSerializer(instance=instance.post).data
            data['comments'] = instance.post_comments.count()
            data['shares'] = instance.post_posts.count()
            data['reacts'] = instance.reacts.count()
        return data