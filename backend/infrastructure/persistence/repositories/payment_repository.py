from typing import Optional
from infrastructure.persistence.models import Payment

class PaymentRepository:
    def create(self, **kwargs) -> Payment:
        return Payment.objects.create(**kwargs)

    def get(self, payment_id: int) -> Payment:
        return Payment.objects.get(pk=payment_id)

    def get_by_idem(self, idempotency_key: str) -> Optional[Payment]:
        try:
            return Payment.objects.get(idempotency_key=idempotency_key)
        except Payment.DoesNotExist:
            return None

    def save(self, payment: Payment) -> Payment:
        payment.save()
        return payment
