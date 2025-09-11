from typing import Iterable
from infrastructure.persistence.models import UserRole, User, Service
from core.shared.utils import haversine_km

def find_freelancers(*, category_id: int | None, lat: float | None, lng: float | None, radius_km: int = 50) -> list[dict]:
    qs = User.objects.filter(role=UserRole.FREELANCE, is_active=True).select_related("profile")
    if category_id:
        # simple: freelancers qui possèdent au moins un service dans la catégorie
        qs = qs.filter(services__category_id=category_id).distinct()
    results: list[dict] = []
    for u in qs:
        d = None
        if lat is not None and lng is not None and u.profile and u.profile.geo_lat and u.profile.geo_lng:
            d = haversine_km(float(lat), float(lng), float(u.profile.geo_lat), float(u.profile.geo_lng))
            if d > radius_km:
                continue
        score = 1.0
        if d is not None:
            score += max(0.0, (radius_km - d) / max(radius_km, 1))
        results.append({"user_id": u.id, "username": u.username, "distance_km": d, "score": round(score, 3)})
    return sorted(results, key=lambda x: (-x["score"], x["distance_km"] or 1e9))
