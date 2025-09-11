from dataclasses import dataclass

@dataclass(frozen=True)
class DisputeCreateInput:
    booking_id: int
    opener_id: int
    reason: str
