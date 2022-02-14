from django.urls import path
from .views import WeatherViewView, UsedWeatherView


urlpatterns = [
    path("post_data/", WeatherViewView.as_view(), name="post_data"),
    path("get_used_files/", UsedWeatherView.as_view(), name="get_used_files")
]
