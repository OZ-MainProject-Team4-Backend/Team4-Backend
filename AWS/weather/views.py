from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from AWS.weather.models import FavoriteLocation, WeatherData
from AWS.weather.serializers import FavoriteLocationSerializer, WeatherDataSerializer


class FavoriteLocationListCreateView(generics.ListCreateAPIView):
    """즐겨찾기 지역 목록 조회 및 추가"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteLocationSerializer

    def get_queryset(self):
        return FavoriteLocation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteLocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """즐겨찾기 지역 수정 및 삭제"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteLocationSerializer

    def get_queryset(self):
        return FavoriteLocation.objects.filter(user=self.request.user)


class CurrentWeatherView(APIView):
    """lat, lon 기반으로 현재 날씨 조회"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")

        if not lat or not lon:
            return Response(
                {"error": "위도(lat)와 경도(lon)가 필요합니다."}, status=400
            )

        weather = (
            WeatherData.objects.filter(
                location__latitude=lat,
                location__longitude=lon,
            )
            .order_by("-fetched_at")
            .first()
        )

        if not weather:
            return Response({"error": "해당 위치의 날씨 정보가 없습니다."}, status=404)

        serializer = WeatherDataSerializer(weather)
        return Response(serializer.data, status=200)


class ForecastWeatherView(APIView):
    """예보 데이터 (샘플, 실제 API 연동은 openweather.py에서)"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")

        if not lat or not lon:
            return Response(
                {"error": "위도(lat)와 경도(lon)가 필요합니다."}, status=400
            )

        # 실제에선 OpenWeather API 호출 예정
        mock_data = [
            {"day": "Mon", "temperature": 18, "condition": "Clear"},
            {"day": "Tue", "temperature": 20, "condition": "Cloudy"},
            {"day": "Wed", "temperature": 21, "condition": "Rain"},
        ]
        return Response(mock_data, status=200)
