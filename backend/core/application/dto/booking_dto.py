from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class BookingCreateInput:
    client_id: int
    service_id: int | None
    equipment_id: int | None
    start_at: datetime
    end_at: datetime
    location_lat: float | None = None
    location_lng: float | None = None
