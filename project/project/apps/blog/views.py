from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Post, Comment, React, SnippetFile
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from .decorators import SnippetDecorator
from user.permissions import SnippetUpdateDeletePermission
from rest_framework.generics import RetrieveAPIView

class PostView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = (SnippetUpdateDeletePermission,)
        return super().destroy(request, *args, **kwargs)

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = (SnippetUpdateDeletePermission,)
        return super().destroy(request, *args, **kwargs)

class ReplyViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def retrieve(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        self.queryset = comment.comment_replies.all()
        return super().list(request, pk)

class CommentRetrieve(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def retrieve(self, request, pk):
        post = Post.objects.get(pk=pk)
        self.queryset = post.post_comments.all()
        return super().retrieve(request, pk)


@api_view(['post'])
@permission_classes([SnippetUpdateDeletePermission])
@SnippetDecorator
def SnippetReact(request, snippet=None):
    reacts = React.objects.create(user=request.user, react=request.data.get('_react'))
    snippet.reacts.add(reacts)
    return Response({'counts' :snippet.reacts.count() , 'react': True})