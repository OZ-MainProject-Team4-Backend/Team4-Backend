from django.conf import settings
from django.core.mail import EmailMessage


def send_verification_email(email, token):
    subject = "이메일 인증을 완료해주세요."
    verify_url = f"http://localhost:8000/api/auth/verify-email?token={token}"

    message = f"""
    안녕하세요!
    아래의 링크를 클릭하면 이메일 인증이 완료가됩니다! 
    
    {verify_url}
    
    인증 링크는 1시간 후 만료됩니다.
    
    """

    email_message = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    email_message.send(fail_silently=False)


def send_password_reset_email(email, token):
    subject = "비밀번호 재설정 링크입니다."
    reset_url = f"http://localhost:8000/api/users/password-reset/confirm/?token={token}"

    message = f"""
    안녕하세요!
    아래의 링크를 클릭하여 비밀번호를 재설정해주세요.
    
    {reset_url}
    
    이 링크는 1시간 후 만료됩니다.
    
    """

    email_message = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    email_message.send(fail_silently=False)
