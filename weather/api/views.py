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
    get_weather_interpolated_data,
    get_wind_interpolated_data,
    get_wind_speed_interpolated_data,
    insert_data
)

from .services import *


np.set_printoptions(threshold=sys.maxsize)


class WeatherViewView(APIView):

    # def get(self, request, *args, **kwargs):
    #     if kwargs:
    #         queryset = Product.objects.get(pk=kwargs["pk"])
    #         serializer = ProductSerializer(queryset)
    #     else:
    #         queryset = Product.objects.all()
    #         serializer = ProductSerializer(queryset, many=True)
    #     return Response(serializer.data)

    def post(self, request):

        workbook = request.FILES.get("file_for_db")
        filename: str = request.data["file_name"].replace("-", "_")
        if not filename.split(".")[1] == "xlsx":
            return Response({"error": "this type is not supported"}, status=status.HTTP_400_BAD_REQUEST)
        with open(os.path.join(settings.BASE_DIR, f"exels/{filename}"), "wb+") as f:
            for chunk in workbook.chunks():
                f.write(chunk)
        workbook = load_workbook(filename=f"exels/{filename}")
        sheet = workbook.active
        sheet.roww = sheet.max_row - 28
        day = get_day(sheet)
        time = get_time(sheet)
        temperatura = get_temperature_interpolated_data(sheet)
        wind_direction = get_wind_interpolated_data(sheet)
        wind_speed = get_wind_speed_interpolated_data(sheet)
        weather_kod = get_weather_interpolated_data(sheet)

        return Response(insert_data(filename.split(".")[0], sheet, day, time, temperatura, wind_direction, wind_speed, weather_kod))

    # serializer = ProductPostSerializer(data=request.data)
    # if serializer.is_valid():
    #     if not serializer.validated_data.get("slug"):
    #         serializer.validated_data["slug"] = slugify(
    #             serializer.validated_data.get("name")
    #         )
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk):
    #     post = Product.objects.get(pk=pk)
    #     serializer = ProductPostPutSerializer(instance=post, data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, requset, pk):
    #     post = Product.objects.get(pk=pk)
    #     post.delete()
    #     return Response({"message": "Item was succesfully deleted"})


class UsedWeatherView(APIView):

    def get(self, request):

        query = UsedFiles.objects.all()
        serializer = UsedFilesSerializer(query, many=True)

        return Response(serializer.data)
