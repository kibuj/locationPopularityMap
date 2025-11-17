# locations/serializers.py
from rest_framework import serializers
from .models import Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['id', 'name', 'address', 'coordinates','author']
        read_only_fields = ['id', 'author']

