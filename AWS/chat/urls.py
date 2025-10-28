from rest_framework.routers import DefaultRouter

from AWS.chat.views import AiChatlogViewSet, AiModelSettingViewSet

router = DefaultRouter()
router.register(r"chat_logs", AiChatlogViewSet, basename="chat_log")
router.register(
    r"chat_model_settings", AiModelSettingViewSet, basename="chat_model_setting"
)

urlpatterns = router.urls
