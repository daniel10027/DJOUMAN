from infrastructure.persistence.models import CommissionPolicy, Service

def compute_commission(service: Service | None, amount: float) -> tuple[float, float]:
    """
    Retourne (rate%, commission_amount)
    Règles simples : si policy liée à la catégorie existe -> use it, sinon aucune commission.
    """
    if not service:
        return 0.0, 0.0
    policy = CommissionPolicy.objects.filter(service_category=service.category, is_active=True).first()
    if not policy:
        return 0.0, 0.0
    rate = float(policy.rate)
    com = amount * rate / 100.0
    if policy.min_amount and com < float(policy.min_amount):
        com = float(policy.min_amount)
    if policy.max_amount and com > float(policy.max_amount):
        com = float(policy.max_amount)
    return rate, com
