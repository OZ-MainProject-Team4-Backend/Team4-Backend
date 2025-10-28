from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .utils.email_token import generate_email_token
from .utils.send_email import send_verification_email


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=150, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    email_verified = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def soft_delete(self):
        """Soft delete helper"""
        self.deleted_at = timezone.now()
        self.save()

    @property
    def is_active(self):
        return self.deleted_at is None


class EmailVerification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=150)
    code = models.CharField(
        max_length=100
    )  # 토큰 길이가 10자를 넘을 수 있으므로 100으로 변경
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "email_verifications"
        verbose_name = "Email Verification"
        verbose_name_plural = "Email Verifications"

    def __str__(self):
        return f"{self.user.email} - {self.code}"


class SocialAccount(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20)
    provider_user_id = models.CharField(max_length=200)
    connected_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "social_accounts"
        verbose_name = "Social Account"
        verbose_name_plural = "Social Accounts"
        unique_together = ("provider", "provider_user_id")

    def __str__(self):
        return f"{self.user.email} - {self.provider}"


class Token(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_jwt = models.CharField(
        max_length=500, blank=True, null=True
    )  # JWT 길이가 200을 넘을 수 있으므로 500으로 변경
    refresh_jwt = models.CharField(
        max_length=500, blank=True, null=True
    )  # JWT 길이가 200을 넘을 수 있으므로 500으로 변경
    access_expires_at = models.DateTimeField(blank=True, null=True)
    refresh_expires_at = models.DateTimeField(blank=True, null=True)
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "tokens"
        verbose_name = "Token"
        verbose_name_plural = "Tokens"

    def __str__(self):
        return f"Token for {self.user.email}"


# 새로운 유저가 생성될 때 이메일 인증 토큰 생성 및 이메일 발송
@receiver(post_save, sender=User)
def send_verification_email_on_user_creation(sender, instance, created, **kwargs):
    if created and not instance.email_verified:
        token_code = generate_email_token(instance.email)
        token_code = (token_code or "")[:10]
        expires_at = timezone.now() + timedelta(hours=1)  # 1시간 후 만료
        EmailVerification.objects.create(
            user=instance, email=instance.email, code=token_code, expires_at=expires_at
        )
        send_verification_email(instance.email, token_code)
