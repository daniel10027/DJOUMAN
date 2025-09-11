from typing import Iterable
from infrastructure.persistence.models import CommissionPolicy, ServiceCategory

class CommissionRepository:
    def list(self, **filters) -> Iterable[CommissionPolicy]:
        qs = CommissionPolicy.objects.select_related("service_category").all()
        if "active" in filters:
            qs = qs.filter(is_active=bool(filters["active"]))
        if "category" in filters:
            qs = qs.filter(service_category_id=filters["category"])
        return qs.order_by("service_category__name", "id")

    def get(self, policy_id: int) -> CommissionPolicy:
        return CommissionPolicy.objects.get(pk=policy_id)

    def create(self, **kwargs) -> CommissionPolicy:
        return CommissionPolicy.objects.create(**kwargs)

    def activate(self, policy: CommissionPolicy) -> CommissionPolicy:
        policy.is_active = True
        policy.save(update_fields=["is_active"])
        return policy

    def deactivate(self, policy: CommissionPolicy) -> CommissionPolicy:
        policy.is_active = False
        policy.save(update_fields=["is_active"])
        return policy

    def save(self, policy: CommissionPolicy) -> CommissionPolicy:
        policy.save()
        return policy
