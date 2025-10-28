from rest_framework import serializers

from .models import FavoriteLocation, Location, WeatherData, WeatherHistory


# 위치 정보
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "latitude",
            "longitude",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# 즐겨찾기 위치
class FavoriteLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source="location", write_only=True
    )

    class Meta:
        model = FavoriteLocation
        fields = [
            "id",
            "location",
            "location_id",
            "alias",
            "is_default",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


# 날씨 데이터
class WeatherDataSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source="location", write_only=True
    )

    class Meta:
        model = WeatherData
        fields = [
            "id",
            "location",
            "location_id",
            "provider",
            "fetched_at",
            "temperature",
            "feels_like",
            "humidity",
            "wind_speed",
            "rain_probability",
            "condition",
            "raw_payload",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "fetched_at"]


# 과거 날씨 기록
class WeatherHistorySerializer(serializers.ModelSerializer):
    weather_data = WeatherDataSerializer(read_only=True)
    weather_data_id = serializers.PrimaryKeyRelatedField(
        queryset=WeatherData.objects.all(), source="weather_data", write_only=True
    )

    class Meta:
        model = WeatherHistory
        fields = ["id", "weather_data", "weather_data_id", "archived_at", "note"]
        read_only_fields = ["id", "archived_at"]
