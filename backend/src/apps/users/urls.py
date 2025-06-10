from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserDetailView, UserLoginView, UserLogoutView, UserRegisterView

users_patterns = [
    path('me/', UserDetailView.as_view(), name='me'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
]

urlpatterns = [
    path('users/', include(users_patterns), name='users'),
]
