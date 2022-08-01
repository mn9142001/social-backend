from django.urls import path
from .views import UserCreateView, LoginView, ProfileView, block, follow, unfollow
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', UserCreateView.as_view({'post' : 'create'})),
    path('<int:pk>', ProfileView.as_view()),
    path('follow/<int:pk>', follow, name="follow"),
    path('unfollow/<int:pk>', unfollow, name="unfollow"),
    path('block/<int:pk>', block, name="block"),
]