from django.db import models
from AWS.users.models import User
from AWS.weather.models import WeatherData

class AIModelSetting(models.Model):
    name = models.CharField(max_length=150)
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    humidity_min = models.IntegerField(null=True, blank=True)
    humidity_max = models.IntegerField(null=True, blank=True)
    weather_condition = models.CharField(max_length=100, null=True, blank=True)
    category_combo = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.temperature_min}~{self.temperature_max}°C)"


class OutfitRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weather_data = models.ForeignKey(
        WeatherData, on_delete=models.SET_NULL, null=True, blank=True
    )
    model_setting = models.ForeignKey(
        AIModelSetting, on_delete=models.SET_NULL, null=True, blank=True
    )
    rec_1 = models.CharField(max_length=255)
    rec_2 = models.CharField(max_length=255, blank=True, null=True)
    rec_3 = models.CharField(max_length=255, blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_bookmarked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.nickname} 추천: {self.rec_1}"