from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserDetailView, UserLoginView, UserLogoutView, UserRegisterView

users_patterns = [
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path(
        'refresh/',
        (TokenRefreshView.as_view()),
        name='token-refresh',
    ),
]

urlpatterns = [
    path('users/', include(users_patterns)),
]
