from django.urls import path
from .views import PostView, CommentViewSet, ReplyViewSet, CommentRetrieve
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('post', PostView)
router.register('comment', CommentViewSet)
router.register('reply', ReplyViewSet)

urlpatterns = [
    path('comments/<int:pk>', CommentRetrieve.as_view())
] + router.urls