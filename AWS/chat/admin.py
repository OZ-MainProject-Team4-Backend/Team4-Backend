from django.contrib import admin

from AWS.chat.models import AiChatlog


@admin.register(AiChatlog)
class AiChatlogAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "session_id", "created_at")
    list_filter = ("created_at",)
    search_fields = ("session_id", "user_question")
    ordering = ("-created_at",)
