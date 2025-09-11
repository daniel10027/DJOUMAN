from typing import Iterable
from infrastructure.persistence.models import KycDocument, KycStatus

class KycRepository:
    def list(self, **filters) -> Iterable[KycDocument]:
        qs = KycDocument.objects.select_related("user","reviewed_by").all()
        if "user" in filters:
            qs = qs.filter(user_id=filters["user"])
        if "status" in filters:
            qs = qs.filter(status=filters["status"])
        return qs.order_by("-created_at")

    def get(self, kyc_id: int) -> KycDocument:
        return KycDocument.objects.get(pk=kyc_id)

    def create(self, **kwargs) -> KycDocument:
        return KycDocument.objects.create(**kwargs)

    def approve(self, kyc: KycDocument, reviewer_id: int) -> KycDocument:
        from django.utils import timezone
        kyc.status = KycStatus.APPROVED
        kyc.reviewed_by_id = reviewer_id
        kyc.reviewed_at = timezone.now()
        kyc.save(update_fields=["status","reviewed_by","reviewed_at"])
        return kyc

    def reject(self, kyc: KycDocument, reviewer_id: int) -> KycDocument:
        from django.utils import timezone
        kyc.status = KycStatus.REJECTED
        kyc.reviewed_by_id = reviewer_id
        kyc.reviewed_at = timezone.now()
        kyc.save(update_fields=["status","reviewed_by","reviewed_at"])
        return kyc
