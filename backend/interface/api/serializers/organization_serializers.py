from rest_framework import serializers
from infrastructure.persistence.models import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("id","name","slug","status","created_at")
        read_only_fields = ("id","created_at")
