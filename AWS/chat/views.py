from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from google import genai
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

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

    @action(detail=False, methods=["post"])
    def ask_ai(self, request):
        message = request.data.get("message", "")
        if not message:
            return Response({"error": "message 를 입력해주세요."}, status=400)

        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
        )
        return Response({"message": message, "response": response.text})


class AiModelSettingViewSet(viewsets.ModelViewSet):
    queryset = AiModelSetting.objects.all().order_by("updated_at")
    serializer_class = AiModelSettingSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["weather_condition", "active"]
    ordering_fields = ["created_at", "updated_at"]
