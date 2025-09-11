class StripeAdapter:
    def create_intent(self, *, method: str, amount: float, currency: str, idempotency_key: str) -> dict:
        return {"provider_ref": f"stripe_{idempotency_key}"}

    def capture(self, provider_ref: str) -> dict:
        return {"ok": True, "provider_ref": provider_ref}

    def refund(self, provider_ref: str, amount: float | None = None) -> dict:
        return {"ok": True, "provider_ref": provider_ref, "amount": amount}
