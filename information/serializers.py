from rest_framework import serializers

from .models import Station

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        exclude = ['create_at', 'update_at', 'delete_at', 'is_deleted']
