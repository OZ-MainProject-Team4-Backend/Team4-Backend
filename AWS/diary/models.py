from django.db import models

from AWS.users.models import User
from AWS.weather.models import WeatherData


class Diary(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(help_text="작성날짜")
    weather_data = models.ForeignKey(WeatherData, on_delete=models.CASCADE)
    outfit_worn = models.CharField(max_length=255)
    satisfaction = models.IntegerField(help_text="옷차림 만족도 (1~5점")
    notes = models.TextField(help_text="오늘의 체감")
    image_url = models.URLField()
    tags = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'diary'
        verbose_name = 'Diary'
        verbose_name_plural = 'Diaries'

    def __str__(self):
        return str(self.date)
