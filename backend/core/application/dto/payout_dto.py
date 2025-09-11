from dataclasses import dataclass

@dataclass(frozen=True)
class PayoutCreateInput:
    beneficiary_id: int
    amount: float
    currency: str = "XOF"
