from rest_framework import serializers
from infrastructure.persistence.models import Payout

class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ("id","beneficiary","amount","currency","status","created_at")
        read_only_fields = ("id","status","created_at")
