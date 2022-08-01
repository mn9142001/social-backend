from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.viewsets import ModelViewSet
from user.models import User
from .serializers import UserProfileSerializer, UserCreationSerializer
from .permissions import ProfilePermission
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .utils import _unfollow

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

#Sign Up
class UserCreateView(ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = UserCreationSerializer
    queryset = User.objects.all()


#Profile retrival 
class ProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = (ProfilePermission, )

    # get user visiting profile
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['visitor'] = self.request.user
        return context


#allowed get method to try it from url without using any post handler
@permission_classes([ProfilePermission])
@api_view(['post', 'get'])
def follow(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.followers.add(request.user)
    request.user.following.add(user)
    return Response({"followed" : user.followers.count()})

@permission_classes([ProfilePermission])
@api_view(['post', 'get'])
def unfollow(request, pk):
    user = get_object_or_404(User, pk=pk)
    user = _unfollow(user, request.user)
    return Response({"followed" : user.followers.count()})

@permission_classes([ProfilePermission])
@api_view(['post', 'get'])
def block(request, pk):
    user = get_object_or_404(User, pk=pk)
    user = _unfollow(user, request.user)
    request.user.blocked.add(user)
    return Response({"blocked" : True})
