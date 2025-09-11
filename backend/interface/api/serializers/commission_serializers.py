from rest_framework import serializers
from infrastructure.persistence.models import CommissionPolicy, ServiceCategory

class CommissionPolicySerializer(serializers.ModelSerializer):
    service_category = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(), required=False, allow_null=True
    )
    class Meta:
        model = CommissionPolicy
        fields = ("id","service_category","rate","min_amount","max_amount","is_active")
        read_only_fields = ("id",)
