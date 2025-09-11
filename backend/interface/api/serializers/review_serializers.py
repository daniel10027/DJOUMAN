from rest_framework import serializers
from infrastructure.persistence.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id","author","target_user","booking","rating","comment","created_at")
        read_only_fields = ("id","created_at")
