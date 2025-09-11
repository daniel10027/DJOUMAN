from dataclasses import dataclass

@dataclass(frozen=True)
class EquipmentCreateInput:
    owner_id: int
    title: str
    description: str | None = None
    price_per_day: float = 0.0
    deposit: float = 0.0
    currency: str = "XOF"
    photos: list[str] | None = None
    geo_lat: float | None = None
    geo_lng: float | None = None
    is_active: bool = True
