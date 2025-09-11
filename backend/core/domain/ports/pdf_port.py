from typing import Protocol

class PdfPort(Protocol):
    def render_contract(self, *, booking_id: int, context: dict) -> str: ...
