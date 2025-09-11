from rest_framework import serializers

class KPISerializer(serializers.Serializer):
    bookings_count = serializers.IntegerField()
    bookings_amount = serializers.FloatField()
    payments_succeeded = serializers.IntegerField()
    commission_amount = serializers.FloatField()
