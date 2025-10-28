from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.filters import OrderingFilter

from AWS.chat.models import AiChatlog, AiModelSetting
from AWS.chat.serializers import AiChatlogSerializer, AiModelSettingSerializer


class AiChatlogViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AiChatlog.objects.all().order_by("-created_at")
    serializer_class = AiChatlogSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["session_id", "user_id"]
    ordering_fields = ["created_at", "id"]


class AiModelSettingViewSet(viewsets.ModelViewSet):
    queryset = AiModelSetting.objects.all().order_by("updated_at")
    serializer_class = AiModelSettingSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["weather_condition", "active"]
    ordering_fields = ["created_at", "updated_at"]
