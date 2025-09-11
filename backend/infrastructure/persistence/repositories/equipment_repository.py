from infrastructure.persistence.models import Equipment
from core.shared.utils import haversine_km

class EquipmentRepositoryPort: ...
class EquipmentRepository:
    def list(self, **filters):
        qs = Equipment.objects.select_related("owner").filter(is_active=True)
        if "owner" in filters:
            qs = qs.filter(owner_id=filters["owner"])
        lat = filters.get("lat"); lng = filters.get("lng")
        if lat is not None and lng is not None:
            items = []
            for e in qs:
                if e.geo_lat and e.geo_lng:
                    d = haversine_km(float(lat), float(lng), float(e.geo_lat), float(e.geo_lng))
                else:
                    d = None
                items.append((d, e))
            items.sort(key=lambda tup: tup[0] if tup[0] is not None else 1e9)
            return [e for _, e in items]
        return qs.order_by("-id")

    def create(self, **kwargs):
        return Equipment.objects.create(**kwargs)
