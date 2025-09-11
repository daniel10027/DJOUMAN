from django.db.models import Q
from infrastructure.persistence.models import Booking

class BookingRepository:
    def create_booking(self, **kwargs) -> Booking:
        return Booking.objects.create(**kwargs)

    def get(self, booking_id: int) -> Booking:
        return Booking.objects.get(pk=booking_id)

    def save(self, booking: Booking) -> Booking:
        booking.save()
        return booking

    def exists_overlap(self, *, service_id: int | None, equipment_id: int | None, start_at, end_at) -> bool:
        qs = Booking.objects.filter(status__in=["pending","confirmed"])
        if service_id:
            qs = qs.filter(service_id=service_id)
        if equipment_id:
            qs = qs.filter(equipment_id=equipment_id)
        # [start,end) overlap check
        return qs.filter(~(Q(end_at__lte=start_at) | Q(start_at__gte=end_at))).exists()
