from rest_framework import serializers
from infrastructure.persistence.models import Payment, PaymentStatus

class PaymentIntentSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()
    method = serializers.ChoiceField(choices=[("orange_money","Orange Money"),("mtn_momo","MTN MoMo"),("wave","Wave"),("stripe","Stripe")])
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.CharField(max_length=8, default="XOF")
    idempotency_key = serializers.CharField(max_length=120)

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id","booking","method","amount","currency","fees","status","provider_ref","idempotency_key","created_at")
        read_only_fields = ("id","status","provider_ref","created_at")
