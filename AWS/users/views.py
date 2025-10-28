from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import UserSerializer
from .utils.email_token import confirm_email_token

from django.utils import timezone
from .models import User, EmailVerification


User = get_user_model()


class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if User.objects.filter(email=serializer.validated_data["email"]).exists():
            return Response(
                {"error": "이메일 중복"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            {"message": "회원가입 완료. 이메일 인증을 진행하세요."},
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        token_code = request.GET.get("token")

        if not token_code:
            return Response(
                {"error": "토큰이 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            email_verification = EmailVerification.objects.get(
                code=token_code, is_used=False, expires_at__gt=timezone.now()
            )

            user = User.objects.get(email=email_verification.email)

            if user.email_verified:
                return Response(
                    {"message": "이메일이 이미 인증되었습니다."},
                    status=status.HTTP_200_OK,
                )

            user.email_verified = True
            user.save()

            email_verification.is_used = True
            email_verification.save()

            return Response({"message": "이메일 인증 완료!"}, status=status.HTTP_200_OK)

        except EmailVerification.DoesNotExist:
            return Response(
                {"error": "유효하지 않거나 만료된 토큰입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "사용자를 찾을 수 없습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"서버 오류: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "이메일 또는 비밀번호가 올바르지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not check_password(password, user.password):
            return Response(
                {"error": "이메일 또는 비밀번호가 올바르지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.email_verified:
            return Response(
                {"error": "이메일 인증이 필요합니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status=status.HTTP_200_OK,
        )


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"logoutSuccess": True}, status=status.HTTP_200_OK)
        except TokenError:
            return Response(
                {"logoutSuccess": False, "error": "유효하지 않은 토큰입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"logoutSuccess": False, "error": f"서버 오류: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"update": True, "user": serializer.data})
