from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, UniqueConstraint

User = get_user_model()

# 위치
class Location(models.Model):
    name = models.CharField(max_length=150)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "locations"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        return self.name

# 즐겨찾는 위치
class FavoriteLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_locations")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="favorites")
    alias = models.CharField(max_length=100, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "favorite_locations"
        constraints = [
            UniqueConstraint(fields=["user", "location"], name="uq_user_location"),
            UniqueConstraint(fields=["user"], condition=Q(is_default=True), name="uq_user_default_location"),
        ]

    def __str__(self):
        return f"{self.user} - {self.alias or self.location.name}"

# 날씨 데이터
class WeatherData(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="weather_data")
    provider = models.CharField(max_length=50)
    fetched_at = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    humidity = models.IntegerField(blank=True, null=True)
    wind_speed = models.FloatField(blank=True, null=True)
    rain_probability = models.FloatField(blank=True, null=True)
    condition = models.CharField(max_length=100)
    raw_payload = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "weather_data"
        constraints = [
            UniqueConstraint(fields=["location", "provider", "fetched_at"], name="uq_weather_snapshot"),
        ]
        indexes = [
            models.Index(fields=["location"]),
            models.Index(fields=["provider"]),
            models.Index(fields=["condition"]),
        ]

    def __str__(self):
        return f"{self.location.name} - {self.temperature}°C"

# 과거 날씨 보관
class WeatherHistory(models.Model):
    weather_data = models.ForeignKey(WeatherData, on_delete=models.CASCADE, related_name="histories")
    archived_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "weather_history"

    def __str__(self):
        return f"History {self.id} ({self.weather_data_id})"
