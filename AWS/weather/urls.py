from django.urls import path

from . import views

urlpatterns = [
    path(
        "location/favorites/",
        views.FavoriteLocationListCreateView.as_view(),
        name="favorite-location-list-create",
    ),
    path(
        "location/favorites/<int:pk>/",
        views.FavoriteLocationDetailView.as_view(),
        name="favorite-location-detail",
    ),
    path(
        "weather/current/", views.CurrentWeatherView.as_view(), name="current-weather"
    ),
    path(
        "weather/forecast/",
        views.ForecastWeatherView.as_view(),
        name="forecast-weather",
    ),
]
