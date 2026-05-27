from rest_framework import serializers
from .models import DataSource, RawRecord


class DataSourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSource
        fields = '__all__'


class RawRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = RawRecord
        fields = '__all__'