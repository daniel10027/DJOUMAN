from dataclasses import dataclass

@dataclass(frozen=True)
class ContractCreateInput:
    booking_id: int
    file_url: str
