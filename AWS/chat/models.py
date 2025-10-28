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


class AiModelSetting(models.Model):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    humidity_min = models.IntegerField()
    humidity_max = models.IntegerField()
    weather_condition = models.CharField(max_length=100)
    category_combo = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_model_settings"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.name} | {self.weather_condition} ({self.temperature_min}~{self.temperature_max}°C)"