from dataclasses import dataclass
from core.application.dto.payment_dto import PaymentIntentInput, RefundInput
from infrastructure.persistence.models import PaymentStatus

@dataclass
class PaymentUseCases:
    repo: "PaymentRepositoryPort"
    provider: "PaymentProviderPort"

    def create_intent(self, data: PaymentIntentInput):
        # idempotence
        exist = self.repo.get_by_idem(data.idempotency_key)
        if exist:
            return exist
        provider_res = self.provider.create_intent(
            method=data.method, amount=data.amount, currency=data.currency, idempotency_key=data.idempotency_key
        )
        p = self.repo.create(
            booking_id=data.booking_id,
            method=data.method,
            amount=data.amount,
            currency=data.currency,
            status=PaymentStatus.PENDING,
            provider_ref=provider_res["provider_ref"],
            idempotency_key=data.idempotency_key,
        )
        return p

    def capture(self, payment_id: int):
        p = self.repo.get(payment_id)
        res = self.provider.capture(p.provider_ref)
        p.status = PaymentStatus.SUCCEEDED if res.get("ok") else PaymentStatus.FAILED
        return self.repo.save(p)

    def refund(self, data: RefundInput):
        p = self.repo.get(data.payment_id)
        self.provider.refund(p.provider_ref, data.amount)
        p.status = PaymentStatus.REFUNDED
        return self.repo.save(p)
