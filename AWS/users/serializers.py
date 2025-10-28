from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import SocialAccount, Token, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # password 필드 추가 (쓰기 전용)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "nickname",
            "phone",
            "gender",
            "email_verified",
            "created_at",
            "updated_at",
            "password",  # password 필드 포함
        ]
        read_only_fields = (
            "email_verified",
            "created_at",
            "updated_at",
        )  # 읽기 전용 필드 설정

    def create(self, validated_data):
        # validated_data에서 password를 가져와 해싱 후 User 객체 생성
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.password = make_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # password가 validated_data에 있다면 해싱하여 업데이트
        if "password" in validated_data:
            instance.password = make_password(validated_data.pop("password"))
        return super().update(instance, validated_data)


class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ["id", "user", "provider", "provider_user_id", "connected_at"]
        read_only_fields = ["connected_at"]


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = [
            "id",
            "user",
            "access_jwt",
            "refresh_jwt",
            "access_expires_at",
            "refresh_expires_at",
            "revoked",
            "created_at",
        ]
        read_only_fields = ["created_at"]
