from rest_framework import serializers
from infrastructure.persistence.models import Equipment

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ("id","owner","title","description","price_per_day","deposit","currency",
                  "photos","availability_notes","geo_lat","geo_lng","is_active","created_at")
        read_only_fields = ("id","owner","created_at")
