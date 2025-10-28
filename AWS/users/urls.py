from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (LoginView, LogoutView, SignUpView, UserProfileView,
                    VerifyEmailView)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
