from rest_framework import serializers
from infrastructure.persistence.models import User, Service

class MatchingQuerySerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=False)
    lat = serializers.FloatField(required=False)
    lng = serializers.FloatField(required=False)
    radius_km = serializers.IntegerField(required=False, default=50)

class MatchResultSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    distance_km = serializers.FloatField(required=False, allow_null=True)
    score = serializers.FloatField()
