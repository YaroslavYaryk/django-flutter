import imp
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openpyxl import load_workbook
import numpy as np
import sys
import os
from weather.models import UsedFiles
from .serializers import UsedFilesSerializer

from .services.weather import (
    get_day, get_time,
    get_temperature_interpolated_data,
    get_wind_interpolated_data,
    get_wind_speed_interpolated_data,
    insert_data
)
from .services.weather_lagrange import get_all_interpolated_data

from .services import *
from .services.quries_from_db import *


np.set_printoptions(threshold=sys.maxsize)


class WeatherViewView(APIView):

    def get(self, request, table_name):
        return Response(get_all_query_by_table(table_name=table_name))

    def post(self, request):

        workbook = request.FILES.get("file_for_db")
        filename: str = request.data["file_name"].replace("-", "_")
        # method = request.data["method"]
        method = "cubic"
        if not filename.split(".")[1] == "xlsx":
            return Response({"error": "this type is not supported"}, status=status.HTTP_400_BAD_REQUEST)
        with open(os.path.join(settings.BASE_DIR, f"exels/{filename}"), "wb+") as f:
            for chunk in workbook.chunks():
                f.write(chunk)
        workbook = load_workbook(filename=f"exels/{filename}")
        sheet = workbook.active
        day = get_day(sheet)
        time = get_time(sheet)
        if method == "linear":
            temperatura = get_temperature_interpolated_data(sheet)
            wind_direction = get_wind_interpolated_data(sheet)
            wind_speed = get_wind_speed_interpolated_data(sheet)
        elif method == "polinom":
            temperatura, wind_direction, wind_speed = get_all_interpolated_data(
                sheet, method='polynomial', order=2)
        elif method == "cubic":
            temperatura, wind_direction, wind_speed = get_all_interpolated_data(
                sheet, method='cubic')

        return Response(insert_data(filename.split(".")[0], sheet, day, time, temperatura, wind_direction, wind_speed))


class UsedWeatherView(APIView):

    def get(self, request):

        query = UsedFiles.objects.all()
        serializer = UsedFilesSerializer(query, many=True)

        return Response(serializer.data)


class DayWithMaxTempDifferenceView(APIView):

    def get(self, request, *args, **kwargs):

        table_name = request.data["table_name"]

        return Response(get_day_with_max_diff_temperature(table_name=table_name))


class DayWithMaxWindSpeedDifferenceView(APIView):

    def get(self, request, *args, **kwargs):

        table_name = request.data["table_name"]

        return Response(get_day_with_max_diff_wind_speed(table_name=table_name))


class DayWithMaxTempView(APIView):

    def get(self, request, *args, **kwargs):

        table_name = request.data["table_name"]

        return Response(get_day_with_some_temperature(table_name=table_name, slug="max"))


class DayWithMinTempView(APIView):

    def get(self, request, *args, **kwargs):

        table_name = request.data["table_name"]

        return Response(get_day_with_some_temperature(table_name=table_name, slug="min"))


class DayWithMaxWindSpeedView(APIView):

    def get(self, request, *args, **kwargs):

        table_name = request.data["table_name"]

        return Response(get_day_with_some_wind(table_name=table_name, slug="max"))


class DayWithMinWindSpeedView(APIView):

    def get(self, request, *args, **kwargs):

        table_name = request.data["table_name"]

        return Response(get_day_with_some_wind(table_name=table_name, slug="min"))


class DayWithSomeWindDirectionView(APIView):

    def get(self, request, *args, **kwargs):

        table_name = request.data["table_name"]
        wind_direction = request.data["direction"]

        return Response(get_day_with_some_wind_direction(table_name=table_name, wind_direction=wind_direction))
