from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.sites import requests
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import EmailVerification, User, Token, SocialAccount
from .serializers import UserSerializer, TokenSerializer
from .utils.email_token import confirm_email_token

NAVER_CLIENT_ID = "tzzCqjUzSr8JarrORWRF"
NAVER_CLIENT_SECRET = "BOff1kCr8Y"


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
        return Response({"message":"회원가입 완료. 이어서 이메일 인증을 진행하세요."},
        status=status.HTTP_201_CREATED,)


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
        access = refresh.access_token

        Token.objects.create(
            user=user,
            access_jwt= str(access),
            refresh_jwt = str(refresh),
            access_expires_at=timezone.now() + timezone.timedelta(minutes=5),
            refresh_expires_at=timezone.now() + timezone.timedelta(days=7),
        )
        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status=status.HTTP_200_OK,
        )


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"logoutSuccess": False, "error": "refresh 토큰이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            # DB상의 토큰 revoked 처리 (가능하면 일치 토큰을 찾아 무효화)
            db_token = Token.objects.filter(refresh_jwt=refresh_token, revoked=False).first()
            if db_token:
                db_token.revoked = True
                db_token.save()

            return Response({"logoutSuccess": True}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"logoutSuccess": False, "error": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"logoutSuccess": False, "error": f"서버 오류: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

class DeleteUserView(generics.DestroyAPIView):
    permission_classes =  [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.deleted_at = timezone.now()
        user.save()
        return Response({"message":"회원 탈퇴 처리 완료"},status=status.HTTP_200_OK)

class TokenListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TokenSerializer
    queryset = Token.objects.all().order_by("-created_at")

class TokenRevokeView(generics.RetrieveAPIView):
    permission_classes =  [permissions.IsAdminUser]

    def post(self,request,*args,**kwargs):
        token_id =request.data.get("token_id")
        if not token_id:
            return Response({"에러":"token_id 필요합니다"},status=status.HTTP_400_BAD_REQUEST)
        try:
            t = Token.objects.get(id=token_id)
            t.revoked = True
            t.save()
            return Response({"message": "토큰 무효화 완료"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "토큰 없음"}, status=status.HTTP_404_NOT_FOUND)

class NaverLoginView(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        code = request.data.get("code")
        state = request.data.get("state")
        if not code or not state:
            return Response(
                {
                    "에러":"code/state 누락"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        token_url = "https://nid.naver.com/oauth2.0/token"
        token_params = {
            "grant_type": "authorization_code",
            "client_id": "tzzCqjUzSr8JarrORWR",
            "client_secret": "BOff1kCr8Y",
            "code": code,
            "state": state,
        }
        token_res = requests.get(token_url, params=token_params)
        token_data = token_res.json()

        access_token = token_data.get("access_token")
        if not access_token:
            return Response(
                {"error": "토큰 요청 실패", "detail": token_data},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 2️⃣ 네이버 유저 정보 요청
        profile_url = "https://openapi.naver.com/v1/nid/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_res = requests.get(profile_url, headers=headers)
        profile_data = profile_res.json()

        if profile_data.get("resultcode") != "00":
            return Response(
                {"error": "네이버 프로필 요청 실패", "detail": profile_data},
                status=status.HTTP_400_BAD_REQUEST,
            )

        naver_user = profile_data["response"]
        email = naver_user.get("email")
        nickname = naver_user.get("nickname")
        provider_user_id = naver_user.get("id")

        # 3️⃣ User 생성 or 조회
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"nickname": nickname, "email_verified": True, "password": "!"},
        )

        # 4️⃣ SocialAccount 생성 or 조회
        SocialAccount.objects.get_or_create(
            user=user,
            provider="naver",
            provider_user_id=provider_user_id,
        )

        # 5️⃣ JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        Token.objects.create(
            user=user,
            access_jwt=str(access),
            refresh_jwt=str(refresh),
            access_expires_at=timezone.now() + timedelta(minutes=5),
            refresh_expires_at=timezone.now() + timedelta(days=7),
        )

        return Response(
            {
                "access": str(access),
                "refresh": str(refresh),
                "email": user.email,
                "nickname": user.nickname,
            },
            status=status.HTTP_200_OK,
        )


class AdminOnlyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        return Response({"message": "관리자 전용 접근 성공"}, status=status.HTTP_200_OK)