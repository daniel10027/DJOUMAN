from rest_framework import serializers
from infrastructure.persistence.models import Booking, BookingStatus
from datetime import timedelta
from infrastructure.persistence.repositories.booking_repository import BookingRepository

class BookingSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = (
            "id","client","service","equipment","start_at","end_at","status",
            "location_lat","location_lng","price","currency","commission_rate","commission_amount",
            "created_at","days",
        )
        read_only_fields = (
            "id","client","status","price","currency","commission_rate","commission_amount","created_at","days"
        )

    def validate(self, attrs):
        start = attrs.get("start_at")
        end = attrs.get("end_at")
        if start and end and end <= start:
            raise serializers.ValidationError({"end_at": "end_at doit être > start_at"})
        service_id = attrs.get("service").id if attrs.get("service") else None
        equipment_id = attrs.get("equipment").id if attrs.get("equipment") else None
        if start and end and (service_id or equipment_id):
            if BookingRepository().exists_overlap(
                service_id=service_id, equipment_id=equipment_id, start_at=start, end_at=end
            ):
                raise serializers.ValidationError("Créneau indisponible (overlap).")
        return attrs

    @staticmethod
    def compute_days(start, end):
        if not start or not end:
            return 1
        delta = end - start
        days = int((delta + timedelta(seconds=86399)).days)  # ceil jour
        return max(1, days)

    def get_days(self, obj) -> int:
        return self.compute_days(obj.start_at, obj.end_at)
