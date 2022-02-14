from os import read
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from weather.models import UsedFiles


class UsedFilesSerializer(serializers.ModelSerializer):
    """ woman fields"""

    class Meta:
        model = UsedFiles
        fields = "__all__"
