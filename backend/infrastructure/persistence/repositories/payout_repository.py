from typing import Iterable
from infrastructure.persistence.models import Payout, PayoutStatus

class PayoutRepository:
    def list(self, **filters) -> Iterable[Payout]:
        qs = Payout.objects.select_related("beneficiary").all()
        if "beneficiary" in filters:
            qs = qs.filter(beneficiary_id=filters["beneficiary"])
        if "status" in filters:
            qs = qs.filter(status=filters["status"])
        if "created_from" in filters:
            qs = qs.filter(created_at__gte=filters["created_from"])
        if "created_to" in filters:
            qs = qs.filter(created_at__lte=filters["created_to"])
        return qs.order_by("-created_at")

    def get(self, payout_id: int) -> Payout:
        return Payout.objects.get(pk=payout_id)

    def create(self, **kwargs) -> Payout:
        return Payout.objects.create(**kwargs)

    def mark_paid(self, payout: Payout) -> Payout:
        payout.status = PayoutStatus.PAID
        payout.save(update_fields=["status"])
        return payout

    def mark_failed(self, payout: Payout) -> Payout:
        payout.status = PayoutStatus.FAILED
        payout.save(update_fields=["status"])
        return payout

    def save(self, payout: Payout) -> Payout:
        payout.save()
        return payout
