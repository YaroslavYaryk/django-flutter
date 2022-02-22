from django.urls import path
from .views import (
    WeatherViewView, UsedWeatherView,
    DayWithMaxTempDifferenceView,
    DayWithMaxWindSpeedDifferenceView,
    DayWithSomeWindDirectionView,
    DayWithMaxTempView,
    DayWithMaxWindSpeedView,
    DayWithMinTempView,
    DayWithMinWindSpeedView

)

urlpatterns = [
    path("post_data/", WeatherViewView.as_view(), name="post_data"),
    path("get_used_files/", UsedWeatherView.as_view(), name="get_used_files"),
    path("all_data/<table_name>/", WeatherViewView.as_view()),
    path("day/max_temp_difference/", DayWithMaxTempDifferenceView.as_view()),
    path("day/max_wind_difference/", DayWithMaxWindSpeedDifferenceView.as_view()),
    path("day/max_temperature/", DayWithMaxTempView.as_view()),
    path("day/min_temperature/", DayWithMinTempView.as_view()),
    path("day/max_wind_speed/", DayWithMaxWindSpeedView.as_view()),
    path("day/min_wind_speed/", DayWithMinWindSpeedView.as_view()),
    path("day/max_some_wind_direction/", DayWithSomeWindDirectionView.as_view())
]
