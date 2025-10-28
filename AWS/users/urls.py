from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    AdminOnlyView,
    ConfirmPasswordResetView,
    DeleteUserView,
    LoginView,
    LogoutView,
    NaverLoginView,
    RequestPasswordResetView,
    SignUpView,
    TokenListView,
    TokenRevokeView,
    UserProfileView,
    VerifyEmailView,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("delete/", DeleteUserView.as_view(), name="user-delete"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Password Reset
    path(
        "password-reset/request/",
        RequestPasswordResetView.as_view(),
        name="password-reset-request",
    ),
    path(
        "password-reset/confirm/",
        ConfirmPasswordResetView.as_view(),
        name="password-reset-confirm",
    ),
    # Social Login
    path("login/naver/", NaverLoginView.as_view(), name="naver-login"),
    # Admin
    path("admin/tokens/", TokenListView.as_view(), name="token-list"),
    path("admin/tokens/revoke/", TokenRevokeView.as_view(), name="token-revoke"),
    path("admin/test/", AdminOnlyView.as_view(), name="admin-only-test"),
]
