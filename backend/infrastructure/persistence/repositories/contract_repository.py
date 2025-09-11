from typing import Iterable
from infrastructure.persistence.models import Contract

class ContractRepository:
    def list(self, **filters) -> Iterable[Contract]:
        qs = Contract.objects.select_related("booking").all()
        if "booking" in filters:
            qs = qs.filter(booking_id=filters["booking"])
        if "signed" in filters:
            qs = qs.filter(signed_at__isnull=not bool(filters["signed"]))
        return qs.order_by("-created_at")

    def get(self, contract_id: int) -> Contract:
        return Contract.objects.get(pk=contract_id)

    def create(self, **kwargs) -> Contract:
        return Contract.objects.create(**kwargs)

    def sign(self, contract: Contract) -> Contract:
        from django.utils import timezone
        contract.signed_at = timezone.now()
        contract.save(update_fields=["signed_at"])
        return contract

    def save(self, contract: Contract) -> Contract:
        contract.save()
        return contract
