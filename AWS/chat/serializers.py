from rest_framework import serializers

from AWS.chat.models import AiChatlog, AiModelSetting


class AiChatlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiChatlog
        fields = "__all__"
        read_only_fields = ("created_at",)


class AiModelSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiModelSetting
        fields = "__all__"
