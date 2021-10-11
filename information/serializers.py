from .models import Station

from rest_framework import serializers

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        exclude = ['create_at', 'update_at', 'delete_at', 'is_deleted']
