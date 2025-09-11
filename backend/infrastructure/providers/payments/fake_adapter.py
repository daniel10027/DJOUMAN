import uuid

class FakePaymentAdapter:
    """
    Adapter de paiement factice pour dev/staging.
    - create_intent: retourne un provider_ref unique
    - capture: ok=True
    - refund: ok=True
    """
    def create_intent(self, *, method: str, amount: float, currency: str, idempotency_key: str) -> dict:
        return {"provider_ref": f"fake_{method}_{uuid.uuid4().hex}"}

    def capture(self, provider_ref: str) -> dict:
        return {"ok": True, "provider_ref": provider_ref}

    def refund(self, provider_ref: str, amount: float | None = None) -> dict:
        return {"ok": True, "provider_ref": provider_ref, "amount": amount}
