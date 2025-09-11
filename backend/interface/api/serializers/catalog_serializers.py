from rest_framework import serializers
from infrastructure.persistence.models import ServiceCategory, Service

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ("id", "name", "slug", "is_active")

class ServiceSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Service
        fields = ("id", "title", "description", "base_price", "currency", "is_active",
                  "category", "category_id", "owner", "created_at")
        read_only_fields = ("id", "owner", "created_at", "category")
