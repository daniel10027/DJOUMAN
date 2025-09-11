from typing import Iterable, Optional
from infrastructure.persistence.models import Organization

class OrganizationRepository:
    def list(self, **filters) -> Iterable[Organization]:
        qs = Organization.objects.all()
        if "status" in filters:
            qs = qs.filter(status=filters["status"])
        if "search" in filters:
            s = filters["search"]
            qs = qs.filter(name__icontains=s) | qs.filter(slug__icontains=s)
        return qs.order_by("name")

    def get(self, org_id: int) -> Organization:
        return Organization.objects.get(pk=org_id)

    def get_by_slug(self, slug: str) -> Optional[Organization]:
        try:
            return Organization.objects.get(slug=slug)
        except Organization.DoesNotExist:
            return None

    def create(self, **kwargs) -> Organization:
        return Organization.objects.create(**kwargs)

    def save(self, org: Organization) -> Organization:
        org.save()
        return org

    def delete(self, org: Organization) -> None:
        org.delete()
