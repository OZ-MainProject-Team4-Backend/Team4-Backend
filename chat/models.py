from django.db import models
from django.utils import timezone


class AiChatlog(models.Model):
    user_id = models.IntegerField()
    session_id = models.CharField(max_length=200, db_index=True)
    user_question = models.TextField()
    ai_answer = models.TextField(blank=True, null=True)
    context = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = "ai_chat_logs"
        indexes = [models.Index(fields=["session_id", "created_at"], name="ai_logs")]
