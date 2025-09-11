from infrastructure.persistence.models import Mission, Booking

class MissionRepository:
    def get(self, mission_id: int) -> Mission:
        return Mission.objects.get(pk=mission_id)

    def create_for_booking(self, booking_id: int, freelance_id: int) -> Mission:
        b = Booking.objects.get(pk=booking_id)
        return Mission.objects.create(booking=b, freelance_id=freelance_id)

    def save(self, mission: Mission) -> Mission:
        mission.save()
        return mission
