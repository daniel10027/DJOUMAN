from dataclasses import dataclass
from core.application.dto.booking_dto import BookingCreateInput
from infrastructure.persistence.models import BookingStatus

@dataclass
class BookingUseCases:
    bookings: "BookingRepositoryPort"

    def create(self, data: BookingCreateInput):
        booking = self.bookings.create_booking(
            client_id=data.client_id,
            service_id=data.service_id,
            equipment_id=data.equipment_id,
            start_at=data.start_at,
            end_at=data.end_at,
            location_lat=data.location_lat,
            location_lng=data.location_lng,
            status=BookingStatus.PENDING,
        )
        return booking

    def confirm(self, booking_id: int):
        b = self.bookings.get(booking_id)
        b.status = BookingStatus.CONFIRMED
        return self.bookings.save(b)

    def cancel(self, booking_id: int):
        b = self.bookings.get(booking_id)
        b.status = BookingStatus.CANCELLED
        return self.bookings.save(b)
