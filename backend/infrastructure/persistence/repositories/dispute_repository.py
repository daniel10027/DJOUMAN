from typing import Iterable
from infrastructure.persistence.models import Dispute, DisputeStatus

class DisputeRepository:
    def list(self, **filters) -> Iterable[Dispute]:
        qs = Dispute.objects.select_related("booking", "opener").all()
        if "booking" in filters:
            qs = qs.filter(booking_id=filters["booking"])
        if "opener" in filters:
            qs = qs.filter(opener_id=filters["opener"])
        if "status" in filters:
            qs = qs.filter(status=filters["status"])
        return qs.order_by("-created_at")

    def get(self, dispute_id: int) -> Dispute:
        return Dispute.objects.get(pk=dispute_id)

    def create(self, **kwargs) -> Dispute:
        return Dispute.objects.create(**kwargs)

    def set_status(self, dispute: Dispute, status: str) -> Dispute:
        if status not in DisputeStatus.values:
            raise ValueError("Invalid DisputeStatus")
        dispute.status = status
        dispute.save(update_fields=["status"])
        return dispute

    def add_message(self, dispute: Dispute, message: dict) -> Dispute:
        msgs = list(dispute.messages or [])
        msgs.append(message)
        dispute.messages = msgs
        dispute.save(update_fields=["messages"])
        return dispute

    def save(self, dispute: Dispute) -> Dispute:
        dispute.save()
        return dispute
