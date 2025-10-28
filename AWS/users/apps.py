from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AWS.users' # 'users' 대신 'AWS.users'로 변경
