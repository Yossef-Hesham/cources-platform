# accounts/urls.py
from django.urls import path
from .views import RegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='register-user'),
    path('user/login/', LoginView.as_view(), name='login-user'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
