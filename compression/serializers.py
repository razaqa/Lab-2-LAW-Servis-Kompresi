from .models import File
from rest_framework import serializers
import os

class ZipFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
