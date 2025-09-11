from rest_framework import serializers
from infrastructure.persistence.models import Dispute

class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = ("id","booking","opener","reason","messages","status","created_at")
        read_only_fields = ("id","status","created_at")
