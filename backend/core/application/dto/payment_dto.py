from dataclasses import dataclass

@dataclass(frozen=True)
class PaymentIntentInput:
    booking_id: int
    method: str
    amount: float
    currency: str
    idempotency_key: str

@dataclass(frozen=True)
class RefundInput:
    payment_id: int
    amount: float | None = None
