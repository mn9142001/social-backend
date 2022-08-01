from ..models import Comment, SnippetFile
from .post import SharedPostSerializer
from .extra import BaseSnippetSerializer

class SnippetSerializer(BaseSnippetSerializer):

    class Meta(SharedPostSerializer.Meta):
        fields = SharedPostSerializer.Meta.fields


class CommentSerializer(SnippetSerializer):
    
    class Meta:
        model = Comment
        fields = SnippetSerializer.Meta.fields + ('post', 'reply',)

    def create(self, validated_data):
        self._creating = True
        media = validated_data.get('media', [])
        if media:
            SnippetFile.objects.create(media = media[0])
            validated_data['media'] = media
        return Comment.objects.create(**validated_data)


    def to_representation(self, instance : Comment):
        data = super().to_representation(instance)
        if getattr(self, '_creating', False):
            data['comments'] = 0
            data['replies'] = 0
        else:
            data['replies'] = instance.comment_replies.count()
            data['reacts'] = instance.reacts.count()
        return data